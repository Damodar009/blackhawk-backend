import uuid
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.timestamp_mixin import TimestampMixin


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    
    usage_count = Column(Integer, default=0)
    trending_score = Column(Float, default=0.0)

    # Relationship
    posts = relationship("Post", secondary="post_tags", back_populates="tags")
