from fastapi import FastAPI, APIRouter

def include_router(app: FastAPI, router: APIRouter, prefix: str, tag: str):
    """
    Include a router with a prefix and tag.
    """
    app.include_router(router, prefix=f"/api/v1/{prefix}", tags=[tag])
