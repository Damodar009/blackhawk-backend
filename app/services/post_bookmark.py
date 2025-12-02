from sqlalchemy.orm import Session
from app.repositories.post_bookmark import PostBookmarkRepository


class PostBookmarkService:
    """PostBookmark Service."""

    def __init__(self):
        self.bookmark_repo = PostBookmarkRepository()

    def toggle_bookmark(self, post_id: str, user_id: str, db: Session) -> dict:
        """Toggle bookmark status for a post."""
        if self.bookmark_repo.has_bookmarked(post_id, user_id, db):
            self.bookmark_repo.delete_bookmark(post_id, user_id, db)
            is_bookmarked = False
        else:
            self.bookmark_repo.create_bookmark(post_id, user_id, db)
            is_bookmarked = True
            
        bookmarks_count = self.bookmark_repo.count_bookmarks(post_id, db)
        
        return {
            "is_bookmarked": is_bookmarked,
            "bookmarks_count": bookmarks_count
        }
