"""
Tests for GET / endpoint (root redirect)
"""

import pytest


def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follow(client):
    """Test that following the redirect works"""
    response = client.get("/", follow_redirects=True)
    
    # Should successfully reach the static file or return 200
    assert response.status_code == 200
