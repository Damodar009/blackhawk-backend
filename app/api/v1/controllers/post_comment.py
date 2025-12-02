from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.post_comment import PostCommentCreate, PostCommentOut, PostCommentUpdate
from app.services.post_comment import PostCommentService
from app.utils.exceptions import NotFoundError, raise_error
from app.utils.response import paginated_success_response, success_response

post_comment_router = APIRouter()
post_comment_service = PostCommentService()


@post_comment_router.post("", response_model=PostCommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    request: Request,
    comment_data: PostCommentCreate,
    db: Session = Depends(deps.get_db)
):
    try:
        # TODO: Get actual user_id from auth token
        user_id = "dummy_user_id"
        
        comment = post_comment_service.create_comment(comment_data, user_id, db)

        return success_response(
            data=comment.model_dump(mode="json"),
            message="Comment created successfully",
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)


@post_comment_router.get("/{comment_id}", response_model=PostCommentOut, status_code=status.HTTP_200_OK)
def get_comment(
    comment_id: str,
    db: Session = Depends(deps.get_db)
):
    """Get comment by ID."""
    comment = post_comment_service.get_comment_by_id(comment_id, db)
    if not comment:
        raise NotFoundError("Comment not found")
    return success_response(
        data=comment.model_dump(mode="json"),
        message="Comment fetched successfully",
        status_code=status.HTTP_200_OK
    )


@post_comment_router.get("/post/{post_id}", status_code=status.HTTP_200_OK)
def get_post_comments(
    post_id: str,
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db),
):
    try:
        skip = (page - 1) * pageSize
        comments, total = post_comment_service.get_comments_by_post(post_id, db, skip=skip, limit=pageSize)

        return paginated_success_response(
            data=[c.model_dump(mode="json") for c in comments],
            total_count=total,
            limit=pageSize,
            skip=skip,
            message="Comments fetched successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)


@post_comment_router.get("/{parent_id}/replies", status_code=status.HTTP_200_OK)
def get_replies(
    parent_id: str,
    db: Session = Depends(deps.get_db)
):
    """Get replies to a comment."""
    try:
        replies = post_comment_service.get_replies(parent_id, db)
        return success_response(
            data=[r.model_dump(mode="json") for r in replies],
            message="Replies fetched successfully",
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)


@post_comment_router.put("/{comment_id}", response_model=PostCommentOut, status_code=status.HTTP_200_OK)
def update_comment(
    request: Request,
    comment_id: str,
    comment_data: PostCommentUpdate,
    db: Session = Depends(deps.get_db),
):
    try:
        updated_comment = post_comment_service.update_comment(comment_id, comment_data, db)
        if not updated_comment:
            raise NotFoundError("Comment not found")

        return success_response(
            data=updated_comment.model_dump(mode="json"),
            message="Comment updated successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)


@post_comment_router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(
    comment_id: str,
    db: Session = Depends(deps.get_db),
):
    """Soft delete comment by ID."""
    success = post_comment_service.delete_comment(comment_id, db)
    if not success:
        raise NotFoundError("Comment not found")
    return success_response(
        message="Comment deleted successfully",
        status_code=status.HTTP_200_OK
    )
