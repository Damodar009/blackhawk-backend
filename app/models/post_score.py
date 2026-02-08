from sqlalchemy import Column, Float, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class PostScore(Base):
    __tablename__ = "post_scores"

    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True)
    
    engagement_score = Column(Float, default=0.0)
    freshness_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    spam_score = Column(Float, default=0.0)
    report_count = Column(Integer, default=0)
    
    last_computed_at = Column(DateTime, server_default=func.current_timestamp())

    # Relationship
    post = relationship("Post", back_populates="scores")
