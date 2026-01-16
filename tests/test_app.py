import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Unregister first if already present
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response_dup.status_code == 400
    # Unregister
    response_del = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response_del.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
    # Unregister again (should fail)
    response_del2 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response_del2.status_code == 404

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 308)  # Allow redirect or direct
