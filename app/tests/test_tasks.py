import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def task_data():
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "Todo",
        "priority": "High",
        "due_date": "2024-07-31T00:00:00"
    }

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "testpassword"}

@pytest.fixture
def auth_token(user_data):
    """
    Register the user, login, and return a valid JWT token.
    """
    client.post("/api/register", json=user_data)
    response = client.post("/api/login", data=user_data)
    return response.json()["access_token"]

def test_create_task(task_data, auth_token):
    """
    Test creating a task for an authenticated user.
    """
    response = client.post("/api/tasks", json=task_data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == task_data["title"]

def test_get_tasks(auth_token):
    """
    Test retrieving tasks for an authenticated user.
    """
    response = client.get("/api/tasks", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_task(auth_token, task_data):
    """
    Test deleting a task by ID.
    """
    create_response = client.post("/api/tasks", json=task_data, headers={"Authorization": f"Bearer {auth_token}"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/tasks/{task_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert delete_response.status_code == 200
