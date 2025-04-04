"""
Tests specifically for validating deployment configuration.
These don't run in CI but can be used to verify configuration files.
"""
import os
import yaml
import re
import pytest

pytestmark = pytest.mark.deploy

def test_app_yaml_static_handlers():
    """Test that app.yaml has proper static file handlers configured."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    yaml_path = os.path.join(base_dir, 'app.yaml')
    
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check that the required handlers exist
    handlers = config.get('handlers', [])
    assert len(handlers) >= 3, "app.yaml should have at least 3 handlers"
    
    # Check static file handlers
    static_dist_handler = None
    static_handler = None
    
    for handler in handlers:
        if 'static_files' in handler and '/static/dist/' in handler.get('url', ''):
            static_dist_handler = handler
        elif 'static_files' in handler and '/static/' in handler.get('url', '') and '/static/dist/' not in handler.get('url', ''):
            static_handler = handler
    
    # Verify static dist handler
    assert static_dist_handler is not None, "No handler for /static/dist/ found"
    assert 'expiration' in static_dist_handler, "Static dist handler should have expiration"
    assert 'secure' in static_dist_handler, "Static dist handler should have secure: always"
    
    # Verify static handler
    assert static_handler is not None, "No handler for /static/ found"
    assert 'expiration' in static_handler, "Static handler should have expiration"
    assert 'secure' in static_handler, "Static handler should have secure: always"

def test_workflow_static_file_copying():
    """Test that the GitHub Actions workflow correctly copies static files."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    workflow_path = os.path.join(base_dir, '.github', 'workflows', 'deploy.yml')
    
    if not os.path.exists(workflow_path):
        pytest.skip("GitHub workflow file not found")
    
    with open(workflow_path, 'r') as f:
        workflow_content = f.read()
    
    # Check for essential static file copy commands
    assert "mkdir -p ../static/dist/css ../static/dist/js ../static/dist/images" in workflow_content, \
        "Workflow should create css, js, and images directories"
    assert "cp -r dist/css/* ../static/dist/css/" in workflow_content, \
        "Workflow should copy CSS files"
    assert "cp -r dist/js/* ../static/dist/js/" in workflow_content, \
        "Workflow should copy JS files"
    assert "cp -r dist/images/* ../static/dist/images/" in workflow_content, \
        "Workflow should copy image files"
    
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