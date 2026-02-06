"""
Database Models
Simple and clean data structures
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from database import Base


# ============================================================================
# SQLAlchemy Models (Database Tables)
# ============================================================================

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with API keys
    api_keys = relationship("APIKey", back_populates="owner")


class APIKey(Base):
    """API Key model with auto-expiration support"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)  # Auto-expiration
    
    is_active = Column(Boolean, default=True)
    
    # Relationship with user
    owner = relationship("User", back_populates="api_keys")


# ============================================================================
# Pydantic Models (API Request/Response)
# ============================================================================

class UserCreate(BaseModel):
    """Request model for user registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Request model for user login"""
    email: EmailStr
    password: str


class APIKeyCreate(BaseModel):
    """Request model for creating API key"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    expiry_days: Optional[int] = Field(default=90, ge=1, le=365)  # Auto-expire in 90 days by default


class APIKeyResponse(BaseModel):
    """Response model for API key"""
    message: str
    api_key: str  # Full key only shown once during creation
    key_id: int
    name: str
    description: Optional[str]
    created_at: str
    expires_at: Optional[str]
    last_used_at: Optional[str]
    
    class Config:
        from_attributes = True
