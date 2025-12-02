from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base import Base


class PostBookmark(Base):
    __tablename__ = "post_bookmarks"

    post_id = Column(String(36), ForeignKey("posts.id"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
