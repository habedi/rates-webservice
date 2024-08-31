"""This module contains the Flask application factory and database connection string."""

import os

from dotenv import load_dotenv
from flask import Flask

# Loading environment variables from .env file
load_dotenv()


def create_app():
    """Create a Flask application."""
    app = Flask(__name__)

    # Database connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()

    return app


def get_database_uri():
    """Get the database connection string from environment variables."""
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    if None in [db_user, db_password, db_host, db_port, db_name]:
        raise ValueError("Missing required environment variables for database connection :(")

    return f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
