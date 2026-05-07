from flask import Blueprint, request, jsonify, render_template
from app.models import User  # Assuming User is defined in models.py
from werkzeug.security import generate_password_hash
import jwt
import datetime
from flask import current_app as app
import smtplib

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

# Forgot Password Endpoints

@main.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"message": "Email not found!"}), 404

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    # Send email (simplified example, replace with a proper email service)
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your-email@example.com', 'your-email-password')
            server.sendmail(
                'your-email@example.com',
                user.email,
                f"Subject: Password Reset\n\nClick the link to reset your password: http://localhost:3000/reset-password?token={token}"
            )
    except Exception as e:
        return jsonify({"message": "Failed to send email!", "error": str(e)}), 500

    return jsonify({"message": "Password reset link sent!"})

@main.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    try:
        token_data = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(token_data['user_id'])
        if not user:
            return jsonify({"message": "Invalid token!"}), 400

        user.password = generate_password_hash(data['new_password'], method='sha256')
        user.save()  # Assuming a save method is defined in the model
        return jsonify({"message": "Password reset successfully!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 400
    except Exception as e:
        return jsonify({"message": "Invalid token!", "error": str(e)}), 400