"""
Configuration settings for the Flask application.

This file contains the configuration settings for the Flask application. It sets up various
configuration variables, such as the secret key, database URI, and other Flask extensions'
settings.

Classes:
    Config: Base configuration class with default settings, including database URI, secret key,
        and other optional settings like API keys.

Usage:
    Import the Config class in the `create_app` function of the `app` package
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
    
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False