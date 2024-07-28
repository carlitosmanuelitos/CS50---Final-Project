"""
Initialization file for the Stock AI Portfolio Tracking app.

This module creates and configures the Flask application, sets up the database,
and initializes various Flask extensions. It also defines the application factory function.

Variables:
    project_root: The root directory of the project.
    db: SQLAlchemy database instance.
    migrate: Flask-Migrate instance for handling database migrations.
    login_manager: LoginManager instance for handling user sessions.

Functions:
    create_app: Application factory function that creates and configures the Flask app.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from config import Config, TestConfig

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder=os.path.abspath(os.path.join(project_root, 'templates')),
                static_folder=os.path.abspath(os.path.join(project_root, 'static')))
    
    if config_name == 'testing':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from app import models
        from app.routes import auth, main
        
        app.register_blueprint(auth.auth)
        app.register_blueprint(main.main)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app