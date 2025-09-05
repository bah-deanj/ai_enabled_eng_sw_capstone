# tests/test_main_simple_1.py

import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is defined in main.py

client = TestClient(app)

def test_create_user_successful():
    """
    Test that a user is created successfully with valid data.
    """
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "securepassword123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]

def test_create_another_user_successful():
    """
    Test that a second user can be created successfully.
    """
    user_data = {
        "username": "jane_smith",
        "email": "jane@example.com",
        "full_name": "Jane Smith",
        "password": "anothersecurepwd"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]

def test_get_users_returns_created_users():
    """
    Test that the GET /users/ endpoint returns a list including previously created users.
    """
    # Create two users
    user1 = {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice Wonderland",
        "password": "alicepwd"
    }
    user2 = {
        "username": "bob",
        "email": "bob@example.com",
        "full_name": "Bob Builder",
        "password": "bobpwd"
    }
    client.post("/users/", json=user1)
    client.post("/users/", json=user2)

    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    usernames = [user["username"] for user in users]
    assert user1["username"] in usernames
    assert user2["username"] in usernames