from datetime import datetime
from pydantic import BaseModel


class CommentLikeBase(BaseModel):
    comment_id: str
    user_id: str


class CommentLikeCreate(CommentLikeBase):
    pass


class CommentLikeOut(CommentLikeBase):
    created_at: datetime

    class Config:
        from_attributes = True
