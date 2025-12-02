from typing import List, Tuple, Union
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.post_comment import PostComment
from app.schemas.post_comment import PostCommentCreate, PostCommentOut, PostCommentUpdate


class PostCommentRepository:
    """PostComment Repository."""

    def create_comment(self, comment: PostCommentCreate, user_id: str, db: Session) -> PostCommentOut:
        """Create a new comment."""
        db_comment = PostComment(
            id=str(uuid4()),
            user_id=user_id,
            **comment.model_dump()
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return PostCommentOut.model_validate(db_comment)

    def get_comment_by_id(self, id: str, db: Session) -> Union[PostComment, None]:
        """Get comment by ID."""
        return db.query(PostComment).filter(
            PostComment.id == id,
            PostComment.is_deleted == False
        ).first()

    def get_comments_by_post(self, post_id: str, db: Session, skip: int = 0, limit: int = 10) -> Tuple[List[PostCommentOut], int]:
        """Get comments for a post (top-level only)."""
        total = db.query(func.count(PostComment.id)).filter(
            PostComment.post_id == post_id,
            PostComment.parent_id == None,
            PostComment.is_deleted == False
        ).scalar()

        comments = (
            db.query(PostComment)
            .filter(
                PostComment.post_id == post_id,
                PostComment.parent_id == None,
                PostComment.is_deleted == False
            )
            .order_by(PostComment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        comment_out_list = [PostCommentOut.model_validate(comment) for comment in comments]
        return comment_out_list, total

    def get_replies(self, parent_id: str, db: Session) -> List[PostCommentOut]:
        """Get replies to a comment."""
        replies = (
            db.query(PostComment)
            .filter(
                PostComment.parent_id == parent_id,
                PostComment.is_deleted == False
            )
            .order_by(PostComment.created_at.asc())
            .all()
        )
        return [PostCommentOut.model_validate(reply) for reply in replies]

    def update_comment(self, comment_id: str, comment_data: PostCommentUpdate, db: Session) -> PostCommentOut | None:
        """Update comment."""
        comment = self.get_comment_by_id(comment_id, db)
        if not comment:
            return None

        update_data = comment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(comment, key):
                setattr(comment, key, value)

        db.commit()
        db.refresh(comment)
        return PostCommentOut.model_validate(comment)

    def delete_comment(self, id: str, db: Session) -> bool:
        """Soft delete comment."""
        comment = self.get_comment_by_id(id, db)
        if comment:
            comment.is_deleted = True
            db.commit()
            return True
        return False

    def increment_likes_count(self, comment_id: str, db: Session) -> None:
        """Increment likes count."""
        comment = self.get_comment_by_id(comment_id, db)
        if comment:
            comment.likes_count += 1
            db.commit()

    def decrement_likes_count(self, comment_id: str, db: Session) -> None:
        """Decrement likes count."""
        comment = self.get_comment_by_id(comment_id, db)
        if comment and comment.likes_count > 0:
            comment.likes_count -= 1
            db.commit()
