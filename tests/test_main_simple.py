
import pytest
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app, Base, get_db

@pytest.fixture(autouse=True, scope="function")
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Create a new in-memory SQLite database for testing, using StaticPool to share the same DB across connections
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def user_payload():
    return {
        "full_name": "Alice Smith",
        "email": "alice@example.com",
        "user_role": "admin"
    }

@pytest.fixture
def create_user(user_payload):
    # Helper to create user and return response JSON
    response = client.post("/users/", json=user_payload)
    assert response.status_code == 201
    return response.json()

def test_create_user(user_payload):
    response = client.post("/users/", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["full_name"] == user_payload["full_name"]
    assert data["email"] == user_payload["email"]
    assert data["user_role"] == user_payload["user_role"]
    assert "created_at" in data

def test_list_users(create_user, user_payload):
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(u["email"] == user_payload["email"] for u in users)

def test_get_user_by_id(create_user, user_payload):
    user_id = create_user["user_id"]
    response = client.get(f"/users/{user_id}")
def test_create_user():
    # Use a unique email to avoid conflicts with existing data
    unique_email = f"test_{int(time.time())}@example.com"
    # Send a request to create a user
    response = client.post("/users/", json={"email": unique_email, "password": "testpassword"})
    # Assert that the response status code is 200
    assert response.status_code == 200
    user = response.json()
    assert user["user_id"] == user_id
    assert user["email"] == user_payload["email"]
    # Assert that the response email matches the input email
    assert response.json()["email"] == unique_email

def test_update_user(create_user):
    user_id = create_user["user_id"]
    updated_payload = {
        "full_name": "Alice Jones",
        "user_role": "user"
    }
    response = client.put(f"/users/{user_id}", json=updated_payload)
def test_read_users():
    # Create a user first with unique email
    unique_email = f"test_read_{int(time.time())}@example.com"
    client.post("/users/", json={"email": unique_email, "password": "testpassword"})
    
    # Send a request to retrieve the list of users
    response = client.get("/users/")
    # Assert that the response status code is 200
    assert response.status_code == 200
    user = response.json()
    assert user["user_id"] == user_id
    assert user["full_name"] == updated_payload["full_name"]
    assert user["user_role"] == updated_payload["user_role"]
    # Email remains unchanged if not updated
    assert user["email"] == create_user["email"]

def test_delete_user(create_user):
    user_id = create_user["user_id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204 or response.status_code == 200  # FastAPI returns 204 NO CONTENT
    # Confirm user is gone
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404
    # Assert that the response contains a list with at least one user
    assert len(response.json()) > 0