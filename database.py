"""
Database Configuration
Simple SQLite for development, easy to switch to PostgreSQL for production
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - automatically use PostgreSQL on Railway, SQLite locally
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./cybersecurity_platform.db")

# Railway PostgreSQL URLs start with 'postgres://' but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Database dependency for FastAPI
    Creates a new database session for each request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
