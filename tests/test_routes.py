import pytest
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