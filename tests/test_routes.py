import pytest
import os
from flask import url_for, current_app
from bs4 import BeautifulSoup

pytestmark = pytest.mark.routes

def test_index_route(client):
    """Test that the index route returns 200 and contains expected content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data
    
def test_index_svg_links(client):
    """Test that the SVG links in index.html are properly formatted and link to the right routes."""
    response = client.get('/')
    assert response.status_code == 200
    
    # Parse the HTML response
    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Find the Elm script which loads the page
    elm_script = soup.find('script', text=lambda t: t and 'Elm.Home.init' in t)
    assert elm_script is not None, "Elm initialization script not found"
    
    # Test the routes that the links should point to
    expected_routes = ['/about', '/demos', '/resume', '/contact']
    for route in expected_routes:
        # Check if the route is valid
        test_response = client.get(route, follow_redirects=False)
        assert test_response.status_code in [200, 302], f"Route {route} is not valid"

def test_about_route(client):
    """Test that the about route returns 200 and contains expected content."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'html' in response.data

def test_contact_route(client):
    """Test that the contact route returns 200 and contains expected content."""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'html' in response.data

def test_demos_route(client):
    """Test that the demos route returns 200 and contains expected content."""
    response = client.get('/demos')
    assert response.status_code == 200
    assert b'html' in response.data

def test_asteroids_route(client):
    """Test that the asteroids route returns 200 and contains expected content."""
    response = client.get('/asteroids')
    assert response.status_code == 200
    assert b'html' in response.data

def test_resume_redirect(client):
    """Test that the resume route redirects."""
    response = client.get('/resume', follow_redirects=False)
    assert response.status_code == 302  # Should be a redirect

def test_nonexistent_route(client):
    """Test that a nonexistent route returns 404."""
    response = client.get('/nonexistent-route')
    assert response.status_code == 404

def test_static_css_files(client, is_ci_environment):
    """Test that critical CSS files can be accessed."""
    # Test base CSS files that should always be available
    css_files = [
        '/static/css/normalize.css',
        '/static/css/skeleton.css'
    ]
    
    for css_file in css_files:
        response = client.get(css_file)
        assert response.status_code == 200, f"CSS file {css_file} not accessible"
        assert 'text/css' in response.headers['Content-Type']
    
    # Skip dist CSS files in CI environment
    if is_ci_environment:
        pytest.skip("Skipping dist CSS files in CI environment")
    
    # Test dist CSS files in non-CI environment
    dist_css_files = [
        '/static/dist/css/main.css'
    ]
    
    for css_file in dist_css_files:
        response = client.get(css_file)
        assert response.status_code == 200, f"CSS file {css_file} not accessible"
        assert 'text/css' in response.headers['Content-Type']
        
def test_static_js_files(client, is_ci_environment):
    """Test that critical JS files can be accessed."""
    # Skip dist JS files in CI environment
    if is_ci_environment:
        pytest.skip("Skipping JS files in CI environment")
    
    # In non-CI environment, test JS files
    js_files = [
        '/static/dist/js/main.bundle.js',
        '/static/dist/js/vendors.bundle.js'
    ]
    
    for js_file in js_files:
        response = client.get(js_file)
        assert response.status_code == 200, f"JS file {js_file} not accessible"
        assert 'javascript' in response.headers['Content-Type'].lower()

def test_debug_static_endpoint(client):
    """Test the debug static endpoint lists files correctly."""
    response = client.get('/debug/static')
    assert response.status_code == 200
    data = response.json
    
    # Basic structure checks
    assert 'static_folder' in data
    assert 'files' in data
    assert isinstance(data['files'], list)
    
    # Check that we have at least some files
    assert len(data['files']) > 0
    
    # Check that each file entry has the expected structure
    for file_entry in data['files']:
        assert 'path' in file_entry
        assert 'url' in file_entry

def test_favicon_route(client):
    """Ensure the favicon route returns the icon"""
    response = client.get('/favicon.ico')
    assert response.status_code == 200
    assert 'image' in response.headers['Content-Type']


def test_favicon_fallback(client, monkeypatch):
    """Ensure the favicon route falls back when dist icon is missing."""
    dist_path = os.path.join(current_app.static_folder, 'dist', 'images', 'favicon.png')
    fallback_path = os.path.join(current_app.static_folder, 'images', 'favicon.png')

    real_exists = os.path.exists

    def fake_exists(path):
        if path == dist_path:
            return False
        return real_exists(path)

    monkeypatch.setattr(os.path, 'exists', fake_exists)

    with open(fallback_path, 'rb') as f:
        expected_data = f.read()

    response = client.get('/favicon.ico')
    assert response.status_code == 200
    assert response.data == expected_data

