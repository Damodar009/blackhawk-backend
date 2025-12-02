from fastapi import FastAPI
from app.api.v1.controllers import (
    users_router,
    post_router,
    post_like_router,
    post_bookmark_router,
    post_comment_router,
    comment_like_router,
)
from app.core import include_router

def get_routers(app: FastAPI):
    """
    Register all routers.
    """
    routers = [
        include_router(app, users_router, 'users', "Users"),
        include_router(app, post_router, 'posts', "Posts"),
        include_router(app, post_like_router, 'post_likes', "Post Likes"),
        include_router(app, post_bookmark_router, 'post_bookmarks', "Post Bookmarks"),
        include_router(app, post_comment_router, 'post_comments', "Post Comments"),
        include_router(app, comment_like_router, 'comment_likes', "Comment Likes"),
    ]

    return routers
