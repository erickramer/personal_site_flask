import pytest
import os
import sys
import tempfile
import json

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db as _db
from sentiment.models import Tweet

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    
    # Create the database and load test data
    with app.app_context():
        _db.create_all()
        # Create test data
        test_tweet = Tweet("I love this app! 😊")
        _db.session.add(test_tweet)
        _db.session.commit()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='session')
def db(app):
    """Create a database object for tests."""
    with app.app_context():
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for each test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    session = db.session
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(app):
    """A test client for the app."""
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()