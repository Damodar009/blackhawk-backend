import uuid
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.timestamp_mixin import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    bio = Column(String(500), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    location = Column(String(100), nullable=True)
    
    # Preferences
    language = Column(String(10), default='en')
    theme = Column(String(20), default='dark')
    notifications_enabled = Column(Boolean, default=True)
    
    # Status
    last_login_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Full name (kept for backward compatibility if needed, or can be removed)
    full_name = Column(String(255), index=True)
