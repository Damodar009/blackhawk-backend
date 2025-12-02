from datetime import datetime
from pydantic import BaseModel


class PostLikeBase(BaseModel):
    post_id: str
    user_id: str


class PostLikeCreate(PostLikeBase):
    pass


class PostLikeOut(PostLikeBase):
    created_at: datetime

    class Config:
        from_attributes = True
