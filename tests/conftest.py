import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    yield app

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

@pytest.fixture
def is_ci_environment():
    """Determine if we're running in a CI environment."""
    # Common CI environment variables
    ci_env_vars = [
        'CI',
        'GITHUB_ACTIONS',
        'TRAVIS',
        'CIRCLECI', 
        'JENKINS_URL',
        'GITLAB_CI'
    ]
    
    for var in ci_env_vars:
        if os.environ.get(var):
            return True
    
    # Also check if dist directory exists as a heuristic
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dist_dir = os.path.join(base_dir, 'static', 'dist')
    if not os.path.exists(dist_dir):
        return True
        
    return False
