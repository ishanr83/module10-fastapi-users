from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from typing import List
from app.database import engine, get_db, Base
from app.models import User
from app.schemas import UserCreate, UserRead
from app.auth import hash_password

# Create database tables
Base.metadata.create_all(bind=engine)  # pragma: no cover

app = FastAPI(
    title="Secure User Management API",
    description="FastAPI application with secure user authentication, Pydantic validation, and Docker deployment",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Secure User Management API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "users": "/users"
        }
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify database connectivity"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:  # pragma: no cover
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with hashed password.
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address (unique)
    - **password**: Password (minimum 8 characters)
    """
    try:
        # Hash the password
        hashed_password = hash_password(user.password)
        
        # Create user object
        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password
        )
        
        # Add to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        elif "email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        else:  # pragma: no cover
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed"
            )

@app.get("/users", response_model=List[UserRead])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all users with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by ID.
    
    - **user_id**: User ID to retrieve
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    
    - **user_id**: User ID to delete
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return None
