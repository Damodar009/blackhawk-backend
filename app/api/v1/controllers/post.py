from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.services.post import PostService
from app.utils.exceptions import NotFoundError, raise_error
from app.utils.response import paginated_success_response, success_response

post_router = APIRouter()
post_service = PostService()


@post_router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    request: Request,
    post_data: PostCreate,
    db: Session = Depends(deps.get_db)
):
    try:
        # TODO: Add authentication and authorization checks here
        # For now, we skip the staff/user check as get_current_user is missing
        
        # Create post
        post = post_service.create_post(post_data, db)

        return success_response(
            data=post.model_dump(mode="json"),
            message="Post created successfully",
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)


@post_router.get("/{post_id}", response_model=PostOut, status_code=status.HTTP_200_OK)
def get_post(
    post_id: str,
    db: Session = Depends(deps.get_db)
):
    """Get post by ID."""
    post = post_service.get_post_by_id(post_id, db)
    if not post:
        raise NotFoundError("Post not found")
    return success_response(
        data=PostOut.model_validate(post).model_dump(mode="json"),
        message="Post fetched successfully",
        status_code=status.HTTP_200_OK
    )


@post_router.get("", status_code=status.HTTP_200_OK)
def get_all_posts(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db),
):
    try:
        skip = (page - 1) * pageSize
        posts, total = post_service.get_all_posts(db, skip=skip, limit=pageSize)

        return paginated_success_response(
            data=[p.model_dump(mode="json") for p in posts],
            total_count=total,
            limit=pageSize,
            skip=skip,
            message="Posts fetched successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)


@post_router.put("/{post_id}", response_model=PostOut, status_code=status.HTTP_200_OK)
def update_post(
    request: Request,
    post_id: str,
    post_data: PostUpdate,
    db: Session = Depends(deps.get_db),
):
    try:
        # Check if post exists
        existing_post = post_service.get_post_by_id(post_id, db)
        if not existing_post:
            raise NotFoundError("Post not found")

        # Update post
        updated_post = post_service.update_post(post_id, post_data, db)
        if not updated_post:
            raise NotFoundError("Post not found")

        return success_response(
            data=updated_post.model_dump(mode="json"),
            message="Post updated successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise_error(str(e), status.HTTP_400_BAD_REQUEST)


@post_router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(
    post_id: str,
    db: Session = Depends(deps.get_db),
):
    """Soft delete post by ID."""
    success = post_service.delete_post(post_id, db)
    if not success:
        raise NotFoundError("Post not found")
    return success_response(
        message="Post deleted successfully",
        status_code=status.HTTP_200_OK
    )
