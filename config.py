"""
Configuration settings for the Flask application.

This file contains the configuration settings for the Flask application. It sets up various
configuration variables, such as the secret key, database URI, and other Flask extensions'
settings.

Imports:
    import os: Imports the operating system module to interact with the file system.

Classes:
    Config: Base configuration class with default settings, including database URI, secret key,
        and other optional settings like API keys.

Attributes:
    SECRET_KEY (str): Secret key for session management.
    SQLALCHEMY_DATABASE_URI (str): Database URI for SQLAlchemy.
    SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to disable modification tracking for SQLAlchemy.
    OPENAI_API_KEY (str, optional): API key for OpenAI integration.
    NEWS_API_KEY (str, optional): API key for news API integration.

Usage:
    Import the desired configuration class in the `create_app` function of the `app` package
    to configure the Flask application.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Add other configuration variables here, such as API keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')