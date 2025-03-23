import pytest
from flask import url_for, current_app

pytestmark = pytest.mark.routes

def test_index_route(client):
    """Test that the index route returns 200 and contains expected content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data

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