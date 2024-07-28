"""
Database migration script for the Stock AI Portfolio Tracking app.

This script sets up and handles the database migrations using Flask-Migrate. It imports the
necessary modules and initializes the migration environment.

Imports:
    from flask_migrate import Migrate: Imports the Flask-Migrate extension for handling
        database migrations.
    from app import create_app, db: Imports the application factory function and the SQLAlchemy
        database instance from the `app` package.

Usage:
    Run this script to initialize the migration environment and apply database migrations.

Example:
    $ python migration.py db init
    $ python migration.py db migrate
    $ python migration.py db upgrade

This script should be run from the command line to manage database migrations. It utilizes
Flask-Migrate to integrate Alembic with Flask and SQLAlchemy, enabling easy database schema
changes.

"""
from flask_migrate import Migrate
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

