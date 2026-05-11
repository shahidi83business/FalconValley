from flask import Blueprint, request, jsonify, render_template
from flask import current_app as app
from werkzeug.security import generate_password_hash
import jwt
import datetime
import smtplib

from ..models import (
    User,
    UserProfile,
    RoundSession,
    Scenario,
    EconomyFunction,
    Opponent,
)

auth_bp = Blueprint("auth", __name__)

def _serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'updated_at': user.updated_at.isoformat() if user.updated_at else None,
    }


def _get_bearer_token():
    auth_header = request.headers.get('Authorization', '')
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        return parts[1]
    return None


@auth_bp.route('/')
def home():
    return render_template('index.html')


# ---------------------------------------------------------------------------
# Forgot Password Endpoints
# ---------------------------------------------------------------------------

@auth_bp.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json or {}
    user = User.objects(email=data.get('email')).first()
    if not user:
        return jsonify({"message": "Email not found!"}), 404

    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        app.config['SECRET_KEY'],
        algorithm='HS256',
    )

    # Send email (simplified example, replace with a proper email service)
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your-email@example.com', 'your-email-password')
            server.sendmail(
                'your-email@example.com',
                user.email,
                f"Subject: Password Reset\n\nClick the link to reset your password: "
                f"http://localhost:3000/reset-password?token={token}",
            )
    except Exception as e:
        return jsonify({"message": "Failed to send email!", "error": str(e)}), 500

    return jsonify({"message": "Password reset link sent!"})


@auth_bp.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.json or {}
    try:
        token_data = jwt.decode(
            data['token'], app.config['SECRET_KEY'], algorithms=['HS256']
        )
        user = User.objects(id=token_data['user_id']).first()
        if not user:
            return jsonify({"message": "Invalid token!"}), 400

        user.password = generate_password_hash(data['new_password'])
        user.save()
        return jsonify({"message": "Password reset successfully!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 400
    except Exception as e:
        return jsonify({"message": "Invalid token!", "error": str(e)}), 400


# ---------------------------------------------------------------------------
# Authentication Endpoints
# ---------------------------------------------------------------------------

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.objects(email=data.get('username')).first()
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'message': 'Invalid email or password!'}), 401
    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        app.config['SECRET_KEY'],
        algorithm='HS256',
    )
    return jsonify({'token': token}), 200


@auth_bp.route('/api/auth/me', methods=['GET'])
@auth_bp.route('/auth/me', methods=['GET'])
def auth_me():
    token = _get_bearer_token()
    if not token:
        return jsonify({'message': 'Authorization token is required!'}), 401

    try:
        token_data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

    user = User.objects(id=token_data.get('user_id')).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    return jsonify(_serialize_user(user)), 200


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    if User.objects(email=data.get('email')).first():
        return jsonify({'message': 'User already exists!'}), 400
    new_user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
    )
    new_user.save()
    return jsonify({'message': 'User registered successfully!'}), 201

