from sqlalchemy import Column, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.types import UUID
from app.db.base import Base


class PostTag(Base):
    __tablename__ = "post_tags"

    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
    
    relevance_weight = Column(Float, default=1.0)
    created_at = Column(DateTime, server_default=func.current_timestamp())
