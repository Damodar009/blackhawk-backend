from sqlalchemy.orm import Session

from app.repositories.comment_like import CommentLikeRepository
from app.repositories.post_comment import PostCommentRepository


class CommentLikeService:
    """CommentLike Service."""

    def __init__(self):
        self.like_repo = CommentLikeRepository()
        self.comment_repo = PostCommentRepository()

    def toggle_like(self, comment_id: str, user_id: str, db: Session) -> dict:
        """Toggle like status for a comment."""
        if self.like_repo.has_liked(comment_id, user_id, db):
            self.like_repo.delete_like(comment_id, user_id, db)
            self.comment_repo.decrement_likes_count(comment_id, db)
            is_liked = False
        else:
            self.like_repo.create_like(comment_id, user_id, db)
            self.comment_repo.increment_likes_count(comment_id, db)
            is_liked = True
            
        likes_count = self.like_repo.count_likes(comment_id, db)
        
        return {
            "is_liked": is_liked,
            "likes_count": likes_count
        }
