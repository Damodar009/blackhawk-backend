from typing import List, Tuple, Union
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostOut, PostUpdate


class PostRepository:
    """Post Repository."""

    def create_post(self, post: PostCreate, db: Session) -> PostOut:
        """Create a new post in database."""
        db_post = Post(
            id=str(uuid4()),
            **post.model_dump()
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return PostOut.model_validate(db_post)

    def get_post_by_id(self, id: str, db: Session) -> Union[Post, None]:
        """Get post by ID."""
        return db.query(Post).filter(Post.id == id, Post.deleted_at == None).first()

    def get_all_posts(self, db: Session, skip: int = 0, limit: int = 10) -> Tuple[List[PostOut], int]:
        """
        Fetch paginated post list and total count.
        
        Returns:
            (post_list, total_count)
        """
        # Get total posts (excluding deleted)
        total = db.query(func.count(Post.id)).filter(Post.deleted_at == None).scalar()

        # Fetch paginated posts
        post_list = (
            db.query(Post)
            .filter(Post.deleted_at == None)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Convert to PostOut schema
        post_out_list = [PostOut.model_validate(post) for post in post_list]
        return post_out_list, total

    def update_post(self, post_id: str, post_data: PostUpdate, db: Session) -> PostOut | None:
        """Update post in the database."""
        post = self.get_post_by_id(post_id, db)
        if not post:
            return None

        update_data = post_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if hasattr(post, key):
                setattr(post, key, value)

        db.commit()
        db.refresh(post)
        return PostOut.model_validate(post)

    def delete_post(self, id: str, db: Session) -> bool:
        """Soft delete post by setting deleted_at."""
        post = self.get_post_by_id(id, db)
        if post:
            post.deleted_at = sa.func.now()
            db.commit()
            return True
        return False
