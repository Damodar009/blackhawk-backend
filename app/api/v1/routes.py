from fastapi import FastAPI
from app.api.v1.controllers import (
    users_router,
)
from app.core import include_router

def get_routers(app: FastAPI):
    """
    Register all routers.
    """
    routers = [
        include_router(app, users_router, 'users', "Users"),
    ]

    return routers
