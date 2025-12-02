from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.api import deps
from app.services.post_like import PostLikeService
from app.utils.exceptions import raise_error
from app.utils.response import success_response

post_like_router = APIRouter()
post_like_service = PostLikeService()


@post_like_router.post("/{post_id}/like", status_code=status.HTTP_200_OK)
def toggle_like(
    request: Request,
    post_id: str,
    db: Session = Depends(deps.get_db)
):
    try:
        # TODO: Get actual user_id from auth token
        # For now, we'll use a dummy user_id or extract from request if available
        # In a real scenario: user_id = request.state.user.id
        user_id = "dummy_user_id" 
        
        result = post_like_service.toggle_like(post_id, user_id, db)

        return success_response(
            data=result,
            message="Like status updated successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)
