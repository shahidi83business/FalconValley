import os
from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
    app.config['MONGODB_SETTINGS'] = {
        'db': os.environ.get('MONGODB_DB', 'ecokirom'),
        'host': os.environ.get('MONGODB_HOST', 'mongodb://localhost:27017/ecokirom'),
    }

    db.init_app(app)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
