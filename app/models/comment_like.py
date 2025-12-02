from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base import Base


class CommentLike(Base):
    __tablename__ = "comment_likes"

    comment_id = Column(String(36), ForeignKey("post_comments.id"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
