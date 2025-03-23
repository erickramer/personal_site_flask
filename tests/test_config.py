import pytest
from app import create_app

pytestmark = pytest.mark.unit

def test_development_config():
    """Test development configuration."""
    app = create_app('development')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'].endswith('tweets.db')

def test_testing_config():
    """Test testing configuration."""
    app = create_app('testing')
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'

def test_production_config():
    """Test production configuration."""
    app = create_app('production')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SESSION_COOKIE_SECURE']
    assert app.config['SESSION_COOKIE_HTTPONLY']
    assert app.config['REMEMBER_COOKIE_SECURE']
    assert app.config['REMEMBER_COOKIE_HTTPONLY']