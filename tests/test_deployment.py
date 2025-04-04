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
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.yaml')
    
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