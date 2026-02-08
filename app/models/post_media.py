import uuid
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.timestamp_mixin import TimestampMixin


class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"


class PostMedia(Base, TimestampMixin):
    __tablename__ = "post_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False, index=True)
    
    media_type = Column(SAEnum(MediaType, name='media_type_enum'), nullable=False)
    url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    
    duration_ms = Column(Integer, nullable=True)
    has_audio = Column(Boolean, default=True)
    
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    aspect_ratio = Column(String(20), nullable=True)
    
    position = Column(Integer, default=0)
    
    cdn_provider = Column(String(50), nullable=True)
    file_size_kb = Column(Integer, nullable=True)

    # Relationship
    post = relationship("Post", back_populates="media")
