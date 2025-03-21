import pytest
from fastapi.testclient import TestClient
from app import app, events_db

client = TestClient(app)

test_event = {
    "site": "stubhub",
    "event_name": "Test Event",
    "event_url": "https://www.stubhub.com/test-event",
    "event_date": "2025-08-02",
    "target_price": 100.0,
    "email": "test@example.com"
}

@pytest.fixture(autouse=True)
def clean_test_data():
    # Clean the database before and after each test
    events_db.delete_many({"event_url": test_event["event_url"]})
    yield
    events_db.delete_many({"event_url": test_event["event_url"]})

def test_track_event():
    response = client.post("/track", json=test_event)
    assert response.status_code == 200
    assert response.json() == {"message": "Event added successfully"}

def test_prevent_duplicate_tracking():
    client.post("/track", json=test_event)
    response = client.post("/track", json=test_event)
    assert response.status_code == 400
    assert response.json()["detail"] == "Event is already being tracked"

def test_get_tracked_events():
    client.post("/track", json=test_event)
    response = client.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(event["event_url"] == test_event["event_url"] for event in data)

def test_delete_event_successfully():
    client.post("/track", json=test_event)
    response = client.delete("/events", json={"event_url": test_event["event_url"]})
    assert response.status_code == 200
    assert response.json() == {"message": "Event deleted successfully"}

def test_delete_nonexistent_event():
    response = client.delete("/events", json={"event_url": "https://example.com/not-tracked"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Event is not being tracked"

def test_check_prices_does_not_crash():
    client.post("/track", json=test_event)
    response = client.get("/prices")
    assert response.status_code == 200
