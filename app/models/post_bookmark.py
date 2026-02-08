from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.types import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class PostBookmark(Base):
    __tablename__ = "post_bookmarks"

    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=True)
