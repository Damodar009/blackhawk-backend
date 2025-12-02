import uuid
from enum import Enum
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, JSON
from app.db.base import Base
from app.models.timestamp_mixin import TimestampMixin


class PostType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    TEXT = "TEXT"


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    type = Column(String(20), nullable=False)  # Storing Enum as String
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)

    # Media
    image_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    video_duration = Column(Integer, nullable=True)

    # Attribution
    source = Column(String(255), nullable=True)
    source_url = Column(String(500), nullable=True)
    author_id = Column(String(36), nullable=True)

    # Tags
    tags = Column(JSON, default=list)

    # Timestamps
    published_at = Column(DateTime, nullable=False)
    
    # State flags
    is_active = Column(Boolean, default=True)
