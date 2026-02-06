"""
API Key Management Service
Handles key generation, validation, and auto-expiration
"""
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from models import APIKey


class APIKeyService:
    """Service for managing API keys"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_secure_key(self) -> str:
        """
        Generate a cryptographically secure API key
        Format: prefix_randomstring
        """
        # Generate 32 bytes of random data
        random_bytes = secrets.token_bytes(32)
        
        # Create a secure hash
        key_hash = hashlib.sha256(random_bytes).hexdigest()
        
        # Add prefix for easy identification
        api_key = f"sk_{key_hash[:48]}"
        
        return api_key
    
    def create_api_key(
        self,
        user_id: int,
        name: str,
        description: Optional[str] = None,
        expiry_days: int = 90
    ) -> APIKey:
        """
        Create a new API key with auto-expiration
        
        Args:
            user_id: ID of the user creating the key
            name: Name/label for the key
            description: Optional description
            expiry_days: Number of days until key expires (default 90)
        
        Returns:
            APIKey object with the generated key
        """
        # Generate secure key
        key = self.generate_secure_key()
        
        # Calculate expiration date
        expires_at = datetime.utcnow() + timedelta(days=expiry_days)
        
        # Create API key object
        api_key = APIKey(
            key=key,
            name=name,
            description=description,
            user_id=user_id,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            is_active=True
        )
        
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        
        return api_key
    
    def validate_and_update_usage(self, key: str) -> Optional[APIKey]:
        """
        Validate an API key and update its last_used_at timestamp
        Also checks for expiration
        
        Returns:
            APIKey object if valid, None if invalid/expired
        """
        # Find the key in database
        api_key = self.db.query(APIKey).filter(
            APIKey.key == key,
            APIKey.is_active == True
        ).first()
        
        if not api_key:
            return None
        
        # Check if expired
        if self.is_key_expired(api_key):
            # Deactivate expired key
            api_key.is_active = False
            self.db.commit()
            return None
        
        # Update last_used_at timestamp
        api_key.last_used_at = datetime.utcnow()
        self.db.commit()
        
        return api_key
    
    def is_key_expired(self, api_key: APIKey) -> bool:
        """
        Check if an API key is expired
        
        Args:
            api_key: APIKey object to check
        
        Returns:
            True if expired, False otherwise
        """
        if not api_key.expires_at:
            return False
        
        return datetime.utcnow() > api_key.expires_at
    
    def rotate_key(self, old_key: APIKey) -> APIKey:
        """
        Rotate an API key (create new one, deactivate old one)
        Useful for security best practices
        
        Args:
            old_key: The old APIKey object to rotate
        
        Returns:
            New APIKey object
        """
        # Deactivate old key
        old_key.is_active = False
        self.db.commit()
        
        # Create new key with same settings
        new_key = self.create_api_key(
            user_id=old_key.user_id,
            name=old_key.name,
            description=f"Rotated from key #{old_key.id}",
            expiry_days=90  # Reset expiration
        )
        
        return new_key
    
    def cleanup_expired_keys(self):
        """
        Background task to deactivate all expired keys
        Should be run periodically (e.g., daily cron job)
        """
        now = datetime.utcnow()
        
        expired_keys = self.db.query(APIKey).filter(
            APIKey.expires_at < now,
            APIKey.is_active == True
        ).all()
        
        for key in expired_keys:
            key.is_active = False
        
        self.db.commit()
        
        return len(expired_keys)
