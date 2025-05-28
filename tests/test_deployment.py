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
    
    # Check static file handlers with the updated structure
    static_handler = None
    static_css_handler = None
    static_js_handler = None
    static_images_handler = None
    
    for handler in handlers:
        # Check URL patterns
        url = handler.get('url', '')
        
        if url == '/static':
            static_handler = handler
        elif url == '/static/dist/css':
            static_css_handler = handler
        elif url == '/static/dist/js':
            static_js_handler = handler
        elif url == '/static/dist/images':
            static_images_handler = handler
    
    # Verify base static handler
    assert static_handler is not None, "No handler for /static found"
    assert 'static_dir' in static_handler, "Base static handler should use static_dir"
    assert 'expiration' in static_handler, "Base static handler should have expiration"
    assert 'secure' in static_handler, "Base static handler should have secure: always"
    
    # Verify CSS handler
    assert static_css_handler is not None, "No handler for /static/dist/css found"
    assert 'static_dir' in static_css_handler, "CSS handler should use static_dir"
    assert 'mime_type' in static_css_handler, "CSS handler should specify mime_type"
    assert static_css_handler['mime_type'] == 'text/css', "CSS handler should have text/css mime type"
    assert 'expiration' in static_css_handler, "CSS handler should have expiration"
    assert 'secure' in static_css_handler, "CSS handler should have secure: always"
    
    # Verify JS handler
    assert static_js_handler is not None, "No handler for /static/dist/js found"
    assert 'static_dir' in static_js_handler, "JS handler should use static_dir"
    assert 'mime_type' in static_js_handler, "JS handler should specify mime_type"
    assert static_js_handler['mime_type'] == 'application/javascript', "JS handler should have application/javascript mime type"
    assert 'expiration' in static_js_handler, "JS handler should have expiration"
    assert 'secure' in static_js_handler, "JS handler should have secure: always"
    
    # Verify Images handler
    assert static_images_handler is not None, "No handler for /static/dist/images found"
    assert 'static_dir' in static_images_handler, "Images handler should use static_dir"
    assert 'expiration' in static_images_handler, "Images handler should have expiration"
    assert 'secure' in static_images_handler, "Images handler should have secure: always"

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
