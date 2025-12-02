from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.post_like import PostLike


class PostLikeRepository:
    """PostLike Repository."""

    def create_like(self, post_id: str, user_id: str, db: Session) -> PostLike:
        """Create a new like."""
        db_like = PostLike(post_id=post_id, user_id=user_id)
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like

    def delete_like(self, post_id: str, user_id: str, db: Session) -> bool:
        """Delete a like."""
        db_like = db.query(PostLike).filter(
            PostLike.post_id == post_id,
            PostLike.user_id == user_id
        ).first()
        
        if db_like:
            db.delete(db_like)
            db.commit()
            return True
        return False

    def has_liked(self, post_id: str, user_id: str, db: Session) -> bool:
        """Check if user has liked the post."""
        return db.query(PostLike).filter(
            PostLike.post_id == post_id,
            PostLike.user_id == user_id
        ).first() is not None

    def count_likes(self, post_id: str, db: Session) -> int:
        """Count likes for a post."""
        return db.query(func.count(PostLike.post_id)).filter(
            PostLike.post_id == post_id
        ).scalar()
