import pytest
from pydantic import ValidationError
from app.schemas import UserCreate, UserRead

def test_user_create_valid():
    """Test valid user creation data"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    }
    user = UserCreate(**user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password == "securepass123"

def test_user_create_invalid_email():
    """Test that invalid email raises validation error"""
    user_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "securepass123"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_create_short_username():
    """Test that username shorter than 3 characters raises error"""
    user_data = {
        "username": "ab",
        "email": "test@example.com",
        "password": "securepass123"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_create_short_password():
    """Test that password shorter than 8 characters raises error"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "short"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_create_missing_fields():
    """Test that missing required fields raise validation error"""
    user_data = {"username": "testuser"}
    with pytest.raises(ValidationError):
        UserCreate(**user_data)
