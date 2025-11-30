from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User, UserCreate
from app.services.user_service import user_service

users_router = APIRouter()

@users_router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> User:
    user = user_service.create_user(db, user_in)
    return user

@users_router.get("/{user_id}", response_model=User)
def read_user(
    user_id: str,
    db: Session = Depends(deps.get_db),
) -> User:
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
