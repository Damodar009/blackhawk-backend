import uuid
from enum import Enum
from sqlalchemy import Boolean, Column, String, Text, JSON, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import UUID
from app.db.base import Base
from app.models.timestamp_mixin import TimestampMixin


class PostType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    NEWS = "news"


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    type = Column(SAEnum(PostType, name='post_type_enum'), nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Attribution
    source_name = Column(String(100), nullable=True)
    source_url = Column(String(255), nullable=True)
    author_name = Column(String(100), nullable=True)
    
    # Meta
    tags_cache = Column(JSON, nullable=True)
    language = Column(String(10), nullable=True)
    is_sensitive = Column(Boolean, default=False)
    
    published_at = Column(DateTime, server_default=func.current_timestamp())

    # Relationships
    media = relationship("PostMedia", back_populates="post", cascade="all, delete-orphan")
    metrics = relationship("PostMetric", back_populates="post", uselist=False, cascade="all, delete-orphan")
    scores = relationship("PostScore", back_populates="post", uselist=False, cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="post_tags", back_populates="posts")
    
    # User interactions (if you want relationships for them, otherwise simple FKs in child tables is enough)
    # likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    # comments = relationship("PostComment", back_populates="post", cascade="all, delete-orphan")
