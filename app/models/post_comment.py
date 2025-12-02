import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, ForeignKey
from app.db.base import Base


class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String(36), ForeignKey("posts.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    parent_id = Column(String(36), ForeignKey("post_comments.id"), nullable=True)
    
    content = Column(Text, nullable=False)
    likes_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    is_deleted = Column(Boolean, default=False)
