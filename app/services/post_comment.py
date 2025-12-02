from typing import List, Tuple
from sqlalchemy.orm import Session

from app.repositories.post_comment import PostCommentRepository
from app.schemas.post_comment import PostCommentCreate, PostCommentOut, PostCommentUpdate


class PostCommentService:
    """PostComment Service."""

    def __init__(self):
        self.comment_repo = PostCommentRepository()

    def create_comment(self, comment: PostCommentCreate, user_id: str, db: Session) -> PostCommentOut:
        """Create comment service."""
        return self.comment_repo.create_comment(comment, user_id, db)

    def get_comment_by_id(self, comment_id: str, db: Session) -> PostCommentOut | None:
        """Get comment by ID."""
        comment = self.comment_repo.get_comment_by_id(comment_id, db)
        return PostCommentOut.model_validate(comment) if comment else None

    def get_comments_by_post(self, post_id: str, db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[PostCommentOut], int]:
        """Get all comments for a post."""
        return self.comment_repo.get_comments_by_post(post_id, db, skip, limit)

    def get_replies(self, parent_id: str, db: Session) -> List[PostCommentOut]:
        """Get replies to a comment."""
        return self.comment_repo.get_replies(parent_id, db)

    def update_comment(self, comment_id: str, comment_data: PostCommentUpdate, db: Session) -> PostCommentOut | None:
        """Update comment service."""
        return self.comment_repo.update_comment(comment_id, comment_data, db)

    def delete_comment(self, id: str, db: Session) -> bool:
        """Soft delete comment service."""
        return self.comment_repo.delete_comment(id, db)
