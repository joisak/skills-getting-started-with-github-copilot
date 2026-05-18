"""
Tests for DELETE /activities/{activity_name}/unregister endpoint
"""

import pytest


def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    email = "michael@mergington.edu"  # Already registered for Chess Club
    activity = "Chess Club"
    
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()[activity]["participants"])
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    
    # Verify participant was removed
    response = client.get("/activities")
    new_count = len(response.json()[activity]["participants"])
    assert new_count == initial_count - 1
    assert email not in response.json()[activity]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity returns 404"""
    email = "student@mergington.edu"
    activity = "Non-Existent Activity"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered(client):
    """Test unregister when student is not registered returns 400"""
    email = "not_registered@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_after_signup(client):
    """Test signup then unregister in sequence"""
    email = "test_student@mergington.edu"
    activity = "Drama Club"
    
    # Sign up
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify signup
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify unregister
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]
