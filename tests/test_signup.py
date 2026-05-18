"""
Tests for POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_success(client):
    """Test successful signup for an activity"""
    email = "student@mergington.edu"
    activity = "Chess Club"
    
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()[activity]["participants"])
    
    # Sign up
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    
    # Verify participant was added
    response = client.get("/activities")
    new_count = len(response.json()[activity]["participants"])
    assert new_count == initial_count + 1
    assert email in response.json()[activity]["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity returns 404"""
    email = "student@mergington.edu"
    activity = "Non-Existent Activity"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_registered(client):
    """Test signup when student is already registered returns 400"""
    email = "michael@mergington.edu"  # Already registered for Chess Club
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_different_activities(client):
    """Test signing up for multiple different activities"""
    email = "new_student@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for different activity
    response2 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups succeeded
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Basketball Team"]["participants"]
