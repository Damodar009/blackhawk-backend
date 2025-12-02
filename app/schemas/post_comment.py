from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostCommentBase(BaseModel):
    post_id: str
    content: str
    parent_id: Optional[str] = None


class PostCommentCreate(PostCommentBase):
    pass


class PostCommentUpdate(BaseModel):
    content: Optional[str] = None


class PostCommentOut(PostCommentBase):
    id: str
    user_id: str
    likes_count: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
