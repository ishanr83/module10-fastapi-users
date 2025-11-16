import pytest
from app.auth import hash_password, verify_password

def test_hash_password():
    """Test that password hashing works correctly"""
    password = "testpassword123"
    hashed = hash_password(password)
    
    # Hash should not equal plain password
    assert hashed != password
    
    # Hash should be a string
    assert isinstance(hashed, str)
    
    # Hash should have reasonable length (bcrypt produces 60 chars)
    assert len(hashed) > 50

def test_verify_password_correct():
    """Test password verification with correct password"""
    password = "correctpassword"
    hashed = hash_password(password)
    
    # Correct password should verify
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    """Test password verification with incorrect password"""
    password = "correctpassword"
    wrong_password = "wrongpassword"
    hashed = hash_password(password)
    
    # Wrong password should not verify
    assert verify_password(wrong_password, hashed) is False

def test_different_hashes_same_password():
    """Test that same password produces different hashes (salt randomness)"""
    password = "samepassword"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    # Hashes should be different due to random salt
    assert hash1 != hash2
    
    # But both should verify correctly
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
