
import pytest
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
    assert response.status_code == 200
    user = response.json()
    assert user["user_id"] == user_id
    assert user["email"] == user_payload["email"]

def test_update_user(create_user):
    user_id = create_user["user_id"]
    updated_payload = {
        "full_name": "Alice Jones",
        "user_role": "user"
    }
    response = client.put(f"/users/{user_id}", json=updated_payload)
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

def test_create_user_with_existing_email(user_payload):
    # Create the first user
    response1 = client.post("/users/", json=user_payload)
    assert response1.status_code == 201

    # Attempt to create another user with the same email
    payload_duplicate = {
        "full_name": "Different Name",
        "email": user_payload["email"],
        "user_role": "user"
    }
    response2 = client.post("/users/", json=payload_duplicate)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]

def test_get_non_existent_user():
    # Try to get a user with a high (non-existent) ID
    non_existent_user_id = 99999
    response = client.get(f"/users/{non_existent_user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"