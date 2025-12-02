from datetime import datetime
from pydantic import BaseModel


class PostBookmarkBase(BaseModel):
    post_id: str
    user_id: str


class PostBookmarkCreate(PostBookmarkBase):
    pass


class PostBookmarkOut(PostBookmarkBase):
    created_at: datetime

    class Config:
        from_attributes = True
