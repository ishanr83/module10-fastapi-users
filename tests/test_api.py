import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

# Use test database
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/test_db"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    """Create test database tables before each test, drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_read_root(test_db):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check(test_db):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_user(test_db):
    """Test creating a new user"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "password_hash" not in data
    assert "id" in data

def test_create_duplicate_username(test_db):
    """Test that duplicate username raises error"""
    user_data = {
        "username": "duplicate",
        "email": "user1@example.com",
        "password": "password123"
    }
    # Create first user
    response1 = client.post("/users", json=user_data)
    assert response1.status_code == 201
    
    # Try to create second user with same username
    user_data2 = {
        "username": "duplicate",
        "email": "user2@example.com",
        "password": "password456"
    }
    response2 = client.post("/users", json=user_data2)
    assert response2.status_code == 400
    assert "Username already exists" in response2.json()["detail"]

def test_create_duplicate_email(test_db):
    """Test that duplicate email raises error"""
    user_data = {
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "password123"
    }
    # Create first user
    response1 = client.post("/users", json=user_data)
    assert response1.status_code == 201
    
    # Try to create second user with same email
    user_data2 = {
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "password456"
    }
    response2 = client.post("/users", json=user_data2)
    assert response2.status_code == 400
    assert "Email already exists" in response2.json()["detail"]

def test_get_users(test_db):
    """Test retrieving all users"""
    # Create test users
    users = [
        {"username": "user1", "email": "user1@example.com", "password": "pass1234"},
        {"username": "user2", "email": "user2@example.com", "password": "pass5678"}
    ]
    for user in users:
        client.post("/users", json=user)
    
    # Get all users
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_user_by_id(test_db):
    """Test retrieving a specific user by ID"""
    user_data = {
        "username": "specificuser",
        "email": "specific@example.com",
        "password": "password123"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "specificuser"

def test_get_nonexistent_user(test_db):
    """Test retrieving a user that doesn't exist"""
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_delete_user(test_db):
    """Test deleting a user"""
    user_data = {
        "username": "deleteuser",
        "email": "delete@example.com",
        "password": "password123"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    
    # Verify user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
