from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.comment_like import CommentLike


class CommentLikeRepository:
    """CommentLike Repository."""

    def create_like(self, comment_id: str, user_id: str, db: Session) -> CommentLike:
        """Create a new like."""
        db_like = CommentLike(comment_id=comment_id, user_id=user_id)
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like

    def delete_like(self, comment_id: str, user_id: str, db: Session) -> bool:
        """Delete a like."""
        db_like = db.query(CommentLike).filter(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == user_id
        ).first()
        
        if db_like:
            db.delete(db_like)
            db.commit()
            return True
        return False

    def has_liked(self, comment_id: str, user_id: str, db: Session) -> bool:
        """Check if user has liked the comment."""
        return db.query(CommentLike).filter(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == user_id
        ).first() is not None

    def count_likes(self, comment_id: str, db: Session) -> int:
        """Count likes for a comment."""
        return db.query(func.count(CommentLike.comment_id)).filter(
            CommentLike.comment_id == comment_id
        ).scalar()
