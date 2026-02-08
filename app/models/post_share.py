import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.types import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class PostShare(Base):
    __tablename__ = "post_shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    share_type = Column(String(20), nullable=False) # 'internal', 'external', 'copy_link', 'repost'
    target = Column(String(50), nullable=True) # e.g. 'whatsapp', 'twitter'
    
    created_at = Column(DateTime, server_default=func.current_timestamp(), index=True)
