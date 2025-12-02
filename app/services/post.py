from typing import List, Tuple, Union

from sqlalchemy.orm import Session

from app.models.post import Post
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostOut, PostUpdate


class PostService:
    """Post Service."""

    def __init__(self):
        self.post_repo = PostRepository()

    def create_post(self, post: PostCreate, db: Session) -> PostOut:
        """Create post service."""
        return self.post_repo.create_post(post, db)

    def get_post_by_id(self, post_id: str, db: Session) -> Union[Post, None]:
        """Get post by ID."""
        return self.post_repo.get_post_by_id(post_id, db)

    def get_all_posts(self, db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[PostOut], int]:
        """Get all posts."""
        return self.post_repo.get_all_posts(db, skip, limit)

    def update_post(self, post_id: str, post_data: PostUpdate, db: Session) -> PostOut | None:
        """Update post service."""
        return self.post_repo.update_post(post_id, post_data, db)

    def delete_post(self, id: str, db: Session) -> bool:
        """Soft delete post service."""
        return self.post_repo.delete_post(id, db)
