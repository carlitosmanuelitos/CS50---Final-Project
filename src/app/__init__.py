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
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    if config_name == 'testing':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from . import models
        from .routes import auth, main
        
        app.register_blueprint(auth.auth)
        app.register_blueprint(main.main)

        # Create tables
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app