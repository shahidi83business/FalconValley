import os
from flask import Flask
from flask_mongoengine import MongoEngine
import pkgutil
import importlib
db = MongoEngine()

def register_blueprints(app):

    from . import routes

    for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
        module = importlib.import_module(f"app.routes.{module_name}")

        if hasattr(module, "bp"):
            app.register_blueprint(module.bp)

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
    register_blueprints(app)

    return app
