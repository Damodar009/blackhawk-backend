from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.api import deps
from app.services.comment_like import CommentLikeService
from app.utils.exceptions import raise_error
from app.utils.response import success_response

comment_like_router = APIRouter()
comment_like_service = CommentLikeService()


@comment_like_router.post("/{comment_id}/like", status_code=status.HTTP_200_OK)
def toggle_like(
    request: Request,
    comment_id: str,
    db: Session = Depends(deps.get_db)
):
    try:
        # TODO: Get actual user_id from auth token
        user_id = "dummy_user_id" 
        
        result = comment_like_service.toggle_like(comment_id, user_id, db)

        return success_response(
            data=result,
            message="Like status updated successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)
