from sqlalchemy.orm import Session
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, User

class UserService:
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        return user_repository.create(db, obj_in=user_in)

    def get_user(self, db: Session, user_id: str) -> User:
        return user_repository.get(db, user_id)

user_service = UserService()
