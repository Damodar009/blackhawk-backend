from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.models.post import PostType


class PostBase(BaseModel):
    type: PostType
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    
    # Media
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_duration: Optional[int] = None
    
    # Attribution
    source: Optional[str] = None
    source_url: Optional[str] = None
    author_id: Optional[str] = None
    
    # Tags
    tags: List[str] = []
    
    # State flags
    is_active: bool = True
    published_at: datetime


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostOut(PostBase):
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
