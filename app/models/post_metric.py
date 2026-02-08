import uuid
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.timestamp_mixin import TimestampMixin


class PostMetric(Base, TimestampMixin):
    __tablename__ = "post_metrics"

    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True)
    
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    bookmarks_count = Column(Integer, default=0)

    # Relationship
    post = relationship("Post", back_populates="metrics")
