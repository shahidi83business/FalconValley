from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuration can be added here
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Register blueprints or routes
    # Example: from .routes import main
    # app.register_blueprint(main)

    return app