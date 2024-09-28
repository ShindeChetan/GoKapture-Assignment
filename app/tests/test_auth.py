import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "testpassword"}

def test_register_user(user_data):
    """
    Test user registration functionality.
    Should return status code 200 for successful registration.
    """
    response = client.post("/api/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

def test_login_user(user_data):
    """
    Test user login functionality.
    Should return a JWT token if the credentials are valid.
    """
    client.post("/api/register", json=user_data)
    response = client.post("/api/login", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
