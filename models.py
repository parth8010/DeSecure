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


class Wallet(Base):
    """Quantum-proof crypto wallet model"""
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_id = Column(String, unique=True, index=True, nullable=False)  # Public wallet identifier
    
    # Public keys (can be shared)
    kyber_public_key = Column(Text, nullable=False)  # For encryption (KEM)
    dilithium_public_key = Column(Text, nullable=False)  # For signatures
    
    # Encrypted private keys (never shared)
    encrypted_kyber_private = Column(Text, nullable=False)
    encrypted_dilithium_private = Column(Text, nullable=False)
    encrypted_recovery_seed = Column(Text, nullable=False)
    salt = Column(String, nullable=False)  # Salt used for key derivation
    
    # Metadata
    version = Column(String, default="1.0")
    algorithm = Column(String, default="RSA-2048 (PQC-Ready)")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_unlocked_at = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    # Relationship with user
    owner = relationship("User", backref="wallets")


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


# ============================================================================
# Wallet Pydantic Models
# ============================================================================

class WalletCreate(BaseModel):
    """Request model for creating a wallet"""
    password: str = Field(..., min_length=8, description="Password to encrypt wallet keys")


class WalletUnlock(BaseModel):
    """Request model for unlocking a wallet"""
    wallet_id: str
    password: str


class WalletResponse(BaseModel):
    """Response model for wallet creation"""
    message: str
    wallet_id: str
    kyber_public_key: str
    dilithium_public_key: str
    recovery_phrase: str  # Only shown once during creation
    created_at: str
    algorithm: str
    
    class Config:
        from_attributes = True


class WalletInfo(BaseModel):
    """Response model for wallet info (without sensitive data)"""
    wallet_id: str
    kyber_public_key: str
    dilithium_public_key: str
    created_at: str
    last_unlocked_at: Optional[str]
    algorithm: str
    is_active: bool
    
    class Config:
        from_attributes = True


class SignMessageRequest(BaseModel):
    """Request model for signing a message"""
    wallet_id: str
    password: str
    message: str


class SignMessageResponse(BaseModel):
    """Response model for message signature"""
    message: str
    signature: str
    wallet_id: str
    algorithm: str


class VerifySignatureRequest(BaseModel):
    """Request model for verifying a signature"""
    wallet_id: str
    message: str
    signature: str


class EncryptMessageRequest(BaseModel):
    """Request model for encrypting a message for a recipient"""
    recipient_wallet_id: str
    message: str
    sender_wallet_id: str
    sender_password: str


class DecryptMessageRequest(BaseModel):
    """Request model for decrypting a message"""
    wallet_id: str
    password: str
    encrypted_package: dict
