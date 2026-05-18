"""
Tests for GET /activities endpoint
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Check that we have activities
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Check that known activities are present
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Basketball Team" in activities


def test_get_activities_activity_structure(client):
    """Test that each activity has the expected structure and fields"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Check structure of a specific activity
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    # Check field types
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)
    
    # Check participants are emails (strings)
    for participant in chess_club["participants"]:
        assert isinstance(participant, str)
        assert "@" in participant
