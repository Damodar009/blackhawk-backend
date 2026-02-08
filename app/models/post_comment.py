import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.types import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("post_comments.id"), nullable=True)
    
    content = Column(Text, nullable=False)
    likes_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    is_deleted = Column(Boolean, default=False)
    
    # Relationships
    # replies = relationship("PostComment", backref=backref("parent", remote_side=[id]))
