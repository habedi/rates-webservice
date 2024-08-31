"""Tests for the code in api/__init__.py."""

import os
from unittest.mock import patch

from api import create_app, get_database_uri


@patch.dict(os.environ, {"DB_USER": "user", "DB_PASSWORD": "password", "DB_HOST": "localhost",
                         "DB_PORT": "5432", "DB_NAME": "testdb"})
def test_create_app_with_valid_env():
    """Test if the create_app function returns a Flask application with the correct database URI."""
    app = create_app()
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://user:password@localhost:5432/testdb'


@patch.dict(os.environ, {"DB_USER": "user", "DB_PASSWORD": "password", "DB_HOST": "localhost",
                         "DB_PORT": "5432", "DB_NAME": "testdb"})
def test_get_database_uri_with_valid_env():
    """Test if the get_database_uri function returns the correct database URI."""
    assert get_database_uri() == 'postgresql://user:password@localhost:5432/testdb'
