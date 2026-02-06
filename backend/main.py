"""
Cybersecurity Platform - Backend API Server
Serves both Web and Android applications
"""
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import uvicorn

# Import our modules
from models import User, APIKey, APIKeyCreate, APIKeyResponse, UserCreate, UserLogin
from database import get_db, engine, Base
from auth import create_access_token, verify_token, hash_password, verify_password
from api_key_service import APIKeyService
from sqlalchemy.orm import Session

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Cybersecurity Platform API",
    description="Backend API for Web and Android applications",
    version="1.0.0"
)

# Configure CORS to allow both web and mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    user_id = verify_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Cybersecurity Platform API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (for both web and Android)"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate access token
    access_token = create_access_token(new_user.id)
    
    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username
        },
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/api/auth/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user (for both web and Android)"""
    
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate access token
    access_token = create_access_token(user.id)
    
    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        },
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/api/auth/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "created_at": current_user.created_at.isoformat()
    }


# ============================================================================
# API KEY MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/keys/generate", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
def generate_api_key(
    key_data: APIKeyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a new API key
    - Works for both web and Android
    - Auto-expires if not used (based on expiry_days)
    """
    api_key_service = APIKeyService(db)
    
    # Generate the API key
    api_key = api_key_service.create_api_key(
        user_id=current_user.id,
        name=key_data.name,
        description=key_data.description,
        expiry_days=key_data.expiry_days
    )
    
    return {
        "message": "API key generated successfully",
        "api_key": api_key.key,  # Only shown once!
        "key_id": api_key.id,
        "name": api_key.name,
        "description": api_key.description,
        "created_at": api_key.created_at.isoformat(),
        "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
        "last_used_at": None
    }


@app.get("/api/keys", response_model=list[dict])
def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all API keys for current user (API Key Viewer)
    - Shows masked keys for security
    - Works for both web and Android
    """
    api_key_service = APIKeyService(db)
    
    # Get all keys for user
    keys = db.query(APIKey).filter(
        APIKey.user_id == current_user.id,
        APIKey.is_active == True
    ).all()
    
    result = []
    for key in keys:
        # Check if key is expired
        is_expired = api_key_service.is_key_expired(key)
        
        result.append({
            "key_id": key.id,
            "name": key.name,
            "description": key.description,
            "key_preview": f"{key.key[:8]}...{key.key[-4:]}",  # Masked key
            "created_at": key.created_at.isoformat(),
            "last_used_at": key.last_used_at.isoformat() if key.last_used_at else None,
            "expires_at": key.expires_at.isoformat() if key.expires_at else None,
            "is_expired": is_expired,
            "is_active": key.is_active
        })
    
    return result


@app.get("/api/keys/{key_id}")
def get_api_key_details(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific API key"""
    
    key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == current_user.id
    ).first()
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    api_key_service = APIKeyService(db)
    is_expired = api_key_service.is_key_expired(key)
    
    return {
        "key_id": key.id,
        "name": key.name,
        "description": key.description,
        "key_preview": f"{key.key[:8]}...{key.key[-4:]}",
        "created_at": key.created_at.isoformat(),
        "last_used_at": key.last_used_at.isoformat() if key.last_used_at else None,
        "expires_at": key.expires_at.isoformat() if key.expires_at else None,
        "is_expired": is_expired,
        "is_active": key.is_active
    }


@app.delete("/api/keys/{key_id}", status_code=status.HTTP_200_OK)
def revoke_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke (deactivate) an API key"""
    
    key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == current_user.id
    ).first()
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Deactivate the key
    key.is_active = False
    db.commit()
    
    return {
        "message": "API key revoked successfully",
        "key_id": key.id,
        "name": key.name
    }


@app.post("/api/keys/{key_id}/rotate", response_model=APIKeyResponse)
def rotate_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rotate an API key (generate new key, deactivate old one)"""
    
    old_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == current_user.id
    ).first()
    
    if not old_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    api_key_service = APIKeyService(db)
    
    # Create new key with same settings
    new_key = api_key_service.rotate_key(old_key)
    
    return {
        "message": "API key rotated successfully",
        "api_key": new_key.key,  # Only shown once!
        "key_id": new_key.id,
        "name": new_key.name,
        "description": new_key.description,
        "created_at": new_key.created_at.isoformat(),
        "expires_at": new_key.expires_at.isoformat() if new_key.expires_at else None,
        "last_used_at": None
    }


# ============================================================================
# API KEY VALIDATION ENDPOINT
# ============================================================================

@app.post("/api/keys/validate")
def validate_api_key(
    api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """
    Validate an API key
    - Used by other services to check if API key is valid
    - Updates last_used_at timestamp
    - Checks expiration
    """
    api_key_service = APIKeyService(db)
    
    # Validate the key
    key_obj = api_key_service.validate_and_update_usage(api_key)
    
    if not key_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key"
        )
    
    return {
        "valid": True,
        "user_id": key_obj.user_id,
        "key_name": key_obj.name,
        "message": "API key is valid"
    }


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import os
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Run server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        # Railway handles TLS/HTTPS automatically
    )
