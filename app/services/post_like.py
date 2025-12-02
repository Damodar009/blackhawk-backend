from sqlalchemy.orm import Session
from app.repositories.post_like import PostLikeRepository


class PostLikeService:
    """PostLike Service."""

    def __init__(self):
        self.like_repo = PostLikeRepository()

    def toggle_like(self, post_id: str, user_id: str, db: Session) -> dict:
        """Toggle like status for a post."""
        if self.like_repo.has_liked(post_id, user_id, db):
            self.like_repo.delete_like(post_id, user_id, db)
            is_liked = False
        else:
            self.like_repo.create_like(post_id, user_id, db)
            is_liked = True
            
        likes_count = self.like_repo.count_likes(post_id, db)
        
        return {
            "is_liked": is_liked,
            "likes_count": likes_count
        }

    def get_post_likes(self, post_id: str, db: Session) -> int:
        """Get total likes for a post."""
        return self.like_repo.count_likes(post_id, db)
