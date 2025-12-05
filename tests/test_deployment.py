"""
Tests specifically for validating deployment configuration.
These don't run in CI but can be used to verify configuration files.
"""
import os
import re
import pytest

# Try to import yaml, but don't fail if it's not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    
# Skip all tests in this module if yaml is not available
pytestmark = [
    pytest.mark.deploy,
    pytest.mark.skipif(not YAML_AVAILABLE, reason="PyYAML not installed")
]

def test_app_yaml_static_handlers():
    """Test that app.yaml has proper static file handlers configured."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    yaml_path = os.path.join(base_dir, 'app.yaml')
    
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check that the required handlers exist
    handlers = config.get('handlers', [])
    assert len(handlers) >= 3, "app.yaml should have at least 3 handlers"
    
    # Check static file handler
    static_handler = next((h for h in handlers if h.get('url') == '/static'), None)
    assert static_handler is not None, "No handler for /static found"
    assert static_handler.get('static_dir') == 'static', "Base static handler should point at the static directory"
    assert 'expiration' in static_handler, "Base static handler should have expiration"
    assert static_handler.get('secure') == 'always', "Base static handler should have secure: always"
    assert static_handler.get('http_headers', {}).get('Cache-Control') == 'public, max-age=604800'

    # Ensure no legacy dist handlers remain
    for handler in handlers:
        url = handler.get('url', '')
        assert not url.startswith('/static/dist'), f"Legacy dist handler still present: {url}"

# Removed test_workflow_static_file_copying
    
def test_flask_app_static_config():
    """Test that the Flask app is configured for static files correctly."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from app import create_app
    
    # Test production config
    app = create_app('production')
    
    # Check static folder configuration
    assert os.path.basename(app.static_folder) == 'static', "Static folder should end with 'static'"
    assert app.static_url_path == '/static', "Static URL path should be '/static'"
    
    # Check cache timeout for static files
    assert app.config['SEND_FILE_MAX_AGE_DEFAULT'] == 31536000, "Production should use 1 year cache"


def test_github_workflow_uses_make_deploy():
    """Ensure the deploy workflow calls `make deploy`."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    workflow_path = os.path.join(base_dir, '.github', 'workflows', 'deploy.yml')

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    steps = workflow['jobs']['test-and-deploy']['steps']
    assert any('make deploy' in (step.get('run') or '') for step in steps), (
        "deploy.yml should run 'make deploy'")


def test_app_yaml_min_idle_instances():
    """Ensure app.yaml keeps at least one idle instance warm."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    yaml_path = os.path.join(base_dir, 'app.yaml')

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    scaling = config.get('automatic_scaling', {})
    min_idle = scaling.get('min_idle_instances', 0)
    assert min_idle >= 1, "app.yaml should set min_idle_instances >= 1"
