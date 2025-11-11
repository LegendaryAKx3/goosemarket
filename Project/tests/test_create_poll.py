import pytest
import sys
import os
from datetime import datetime, timedelta, timezone

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from api.index import app
from database import get_supabase

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user():
    """Create a test user and return its ID."""
    supabase = get_supabase()
    
    # Create a test user
    user_data = {
        "auth_id": "00000000-0000-0000-0000-000000000001",
        "balance": 1000,
        "active": True
    }
    
    result = supabase.table("users").insert(user_data).execute()
    user_id = result.data[0]["id"]
    
    yield user_id
    
    # Cleanup
    supabase.table("users").delete().eq("id", user_id).execute()

@pytest.fixture(autouse=True)
def clear_polls():
    """Clear all test polls and trades before and after each test."""
    supabase = get_supabase()
    # Delete all test polls (we'll use a specific range or pattern)
    yield
    # Cleanup after test
    supabase.table("trades").delete().neq("id", 0).execute()  # Clear all trades
    supabase.table("polls").delete().like("title", "Test%").execute()
    supabase.table("polls").delete().like("title", "%Test%").execute()

def test_create_poll_valid(client, test_user):
    """Test creating a poll with valid data."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    payload = {
        "title": "Test: What's your favorite color?",
        "description": "Please vote for your favorite color from the options provided.",
        "ends_at": future_time,
        "public": True,
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 201
    
    data = response.get_json()
    assert "poll" in data
    assert data["poll"]["title"] == "Test: What's your favorite color?"
    assert data["poll"]["description"] == "Please vote for your favorite color from the options provided."
    assert data["poll"]["creator"] == test_user
    assert data["poll"]["public"] is True

def test_create_poll_missing_title(client, test_user):
    """Test creating a poll without a title."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    payload = {
        "description": "This is a description",
        "ends_at": future_time,
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_poll_title_too_short(client, test_user):
    """Test creating a poll with title too short."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    payload = {
        "title": "AB",
        "description": "This is a valid description that is long enough",
        "ends_at": future_time,
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "at least 3 characters" in data["error"]

def test_create_poll_missing_description(client, test_user):
    """Test creating a poll without a description."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    payload = {
        "title": "Test Poll Title",
        "ends_at": future_time,
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "description" in data["error"].lower()

def test_create_poll_description_too_short(client, test_user):
    """Test creating a poll with description too short."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    payload = {
        "title": "Test Poll",
        "description": "Too short",
        "ends_at": future_time,
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "at least 10 characters" in data["error"]

def test_create_poll_past_end_time(client, test_user):
    """Test creating a poll with end time in the past."""
    past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    
    payload = {
        "title": "Test Poll Title",
        "description": "This is a valid description for testing purposes",
        "ends_at": past_time,
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "future" in data["error"].lower()

def test_create_poll_invalid_end_time_format(client, test_user):
    """Test creating a poll with invalid end time format."""
    payload = {
        "title": "Test Poll Title",
        "description": "This is a valid description for testing purposes",
        "ends_at": "invalid-date-format",
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "invalid" in data["error"].lower()

def test_create_poll_missing_creator(client):
    """Test creating a poll without creator."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    payload = {
        "title": "Test Poll Title",
        "description": "This is a valid description for testing purposes",
        "ends_at": future_time
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_poll_invalid_creator(client):
    """Test creating a poll with non-existent creator."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    payload = {
        "title": "Test Poll Title",
        "description": "This is a valid description for testing purposes",
        "ends_at": future_time,
        "creator": 999999
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert "does not exist" in data["error"].lower()

def test_create_poll_without_end_time(client, test_user):
    """Test creating a poll without an end time (should be allowed)."""
    payload = {
        "title": "Test Poll No End",
        "description": "This poll has no specific end time set",
        "public": True,
        "creator": test_user
    }
    
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 201
    
    data = response.get_json()
    assert "poll" in data
    assert data["poll"]["title"] == "Test Poll No End"

def test_create_poll_rate_limiting(client, test_user):
    """Test rate limiting for poll creation."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    # Create 2 polls (should succeed)
    for i in range(2):
        payload = {
            "title": f"Test Rate Limit Poll {i}",
            "description": f"This is test poll number {i} for rate limiting",
            "ends_at": future_time,
            "creator": test_user
        }
        response = client.post('/api/polls', json=payload)
        assert response.status_code == 201
    
    # Third poll should be rate limited
    payload = {
        "title": "Test Third Poll",
        "description": "This should be rate limited",
        "ends_at": future_time,
        "creator": test_user
    }
    response = client.post('/api/polls', json=payload)
    assert response.status_code == 429
    data = response.get_json()
    assert "rate limit" in data["error"].lower()

def test_get_poll_valid(client, test_user):
    """Test retrieving a poll by ID."""
    # First create a poll
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    payload = {
        "title": "Test Get Poll",
        "description": "This poll is for testing retrieval",
        "ends_at": future_time,
        "public": True,
        "creator": test_user
    }
    
    create_response = client.post('/api/polls', json=payload)
    assert create_response.status_code == 201
    poll_id = create_response.get_json()["poll"]["id"]
    
    # Retrieve the poll
    get_response = client.get(f'/api/polls/{poll_id}')
    assert get_response.status_code == 200
    
    data = get_response.get_json()
    assert "poll" in data
    assert data["poll"]["title"] == "Test Get Poll"
    assert data["poll"]["has_ended"] is False

def test_get_poll_not_found(client):
    """Test retrieving a non-existent poll."""
    response = client.get('/api/polls/999999')
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_edit_poll_valid(client, test_user):
    """Test editing a poll before any trades."""
    # Create a poll
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    payload = {
        "title": "Test Original Title",
        "description": "Original description for testing purposes only",
        "ends_at": future_time,
        "public": True,
        "creator": test_user
    }
    
    create_response = client.post('/api/polls', json=payload)
    assert create_response.status_code == 201
    poll_id = create_response.get_json()["poll"]["id"]
    
    # Edit the poll
    new_future_time = (datetime.now(timezone.utc) + timedelta(hours=48)).isoformat()
    edit_payload = {
        "title": "Test Updated Title",
        "description": "Updated description for testing purposes only",
        "ends_at": new_future_time,
        "public": False,
        "creator": test_user
    }
    
    edit_response = client.put(f'/api/polls/{poll_id}', json=edit_payload)
    assert edit_response.status_code == 200
    
    data = edit_response.get_json()
    assert data["poll"]["title"] == "Test Updated Title"
    assert data["poll"]["description"] == "Updated description for testing purposes only"
    assert data["poll"]["public"] is False

def test_edit_poll_wrong_user(client, test_user):
    """Test that only the creator can edit a poll."""
    supabase = get_supabase()
    
    # Create another test user
    user_data = {
        "auth_id": "00000000-0000-0000-0000-000000000002",
        "balance": 1000,
        "active": True
    }
    result = supabase.table("users").insert(user_data).execute()
    other_user_id = result.data[0]["id"]
    
    try:
        # Create a poll
        future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        payload = {
            "title": "Test Creator Poll",
            "description": "This poll tests creator permissions",
            "ends_at": future_time,
            "creator": test_user
        }
        
        create_response = client.post('/api/polls', json=payload)
        assert create_response.status_code == 201
        poll_id = create_response.get_json()["poll"]["id"]
        
        # Try to edit with different user
        edit_payload = {
            "title": "Test Hacked Title",
            "creator": other_user_id
        }
        
        edit_response = client.put(f'/api/polls/{poll_id}', json=edit_payload)
        assert edit_response.status_code == 403
        data = edit_response.get_json()
        assert "creator" in data["error"].lower()
    finally:
        # Cleanup
        supabase.table("users").delete().eq("id", other_user_id).execute()

def test_edit_poll_after_trades(client, test_user):
    """Test that polls cannot be edited after trades are made."""
    supabase = get_supabase()
    
    # Create a poll
    future_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    payload = {
        "title": "Test Trade Lock Poll",
        "description": "This poll tests editing after trades",
        "ends_at": future_time,
        "creator": test_user
    }
    
    create_response = client.post('/api/polls', json=payload)
    assert create_response.status_code == 201
    poll_id = create_response.get_json()["poll"]["id"]
    
    # Simulate a trade by inserting into trades table
    trade_data = {
        "poll_id": poll_id,
        "user_id": test_user,
        "amount": 100
    }
    supabase.table("trades").insert(trade_data).execute()
    
    # Try to edit the poll
    edit_payload = {
        "title": "Test Updated Title After Trade",
        "creator": test_user
    }
    
    edit_response = client.put(f'/api/polls/{poll_id}', json=edit_payload)
    assert edit_response.status_code == 403
    data = edit_response.get_json()
    assert "trade" in data["error"].lower()

def test_edit_poll_not_found(client, test_user):
    """Test editing a non-existent poll."""
    edit_payload = {
        "title": "Test Updated Title",
        "creator": test_user
    }
    
    response = client.put('/api/polls/999999', json=edit_payload)
    assert response.status_code == 404

def test_poll_has_ended_flag(client, test_user):
    """Test that polls show has_ended flag correctly."""
    # Create a poll that ends very soon
    close_time = (datetime.now(timezone.utc) + timedelta(seconds=1)).isoformat()
    payload = {
        "title": "Test Auto-End Poll",
        "description": "This poll ends very soon for testing",
        "ends_at": close_time,
        "creator": test_user
    }
    
    create_response = client.post('/api/polls', json=payload)
    assert create_response.status_code == 201
    poll_id = create_response.get_json()["poll"]["id"]
    
    # Wait for end time to pass
    import time
    time.sleep(2)
    
    # Retrieve the poll - it should show has_ended = True
    get_response = client.get(f'/api/polls/{poll_id}')
    assert get_response.status_code == 200
    
    data = get_response.get_json()
    assert data["poll"]["has_ended"] is True
