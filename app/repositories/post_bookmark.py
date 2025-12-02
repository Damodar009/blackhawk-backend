from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.post_bookmark import PostBookmark


class PostBookmarkRepository:
    """PostBookmark Repository."""

    def create_bookmark(self, post_id: str, user_id: str, db: Session) -> PostBookmark:
        """Create a new bookmark."""
        db_bookmark = PostBookmark(post_id=post_id, user_id=user_id)
        db.add(db_bookmark)
        db.commit()
        db.refresh(db_bookmark)
        return db_bookmark

    def delete_bookmark(self, post_id: str, user_id: str, db: Session) -> bool:
        """Delete a bookmark."""
        db_bookmark = db.query(PostBookmark).filter(
            PostBookmark.post_id == post_id,
            PostBookmark.user_id == user_id
        ).first()
        
        if db_bookmark:
            db.delete(db_bookmark)
            db.commit()
            return True
        return False

    def has_bookmarked(self, post_id: str, user_id: str, db: Session) -> bool:
        """Check if user has bookmarked the post."""
        return db.query(PostBookmark).filter(
            PostBookmark.post_id == post_id,
            PostBookmark.user_id == user_id
        ).first() is not None

    def count_bookmarks(self, post_id: str, db: Session) -> int:
        """Count bookmarks for a post."""
        return db.query(func.count(PostBookmark.post_id)).filter(
            PostBookmark.post_id == post_id
        ).scalar()
