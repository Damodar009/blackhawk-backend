from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import session
from app.core.firebase import verify_token
from app.models.user import User
from app.models.user_auth_provider import UserAuthProvider

security = HTTPBearer()

def get_db() -> Generator:
    yield from session.get_session()

async def get_current_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    try:
        decoded_token = verify_token(token.credentials)
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        firebase_uid = decoded_token.get("uid")
        
        # Check if user exists via Auth Provider
        # We look for the provider 'firebase' which stores the unique Firebase UID
        auth_provider = db.query(UserAuthProvider).filter(
            UserAuthProvider.provider == "firebase",
            UserAuthProvider.provider_user_id == firebase_uid
        ).first()

        if not auth_provider:
            # Fallback: check by email if present in token
            email = decoded_token.get("email")
            if email:
                user = db.query(User).filter(User.email == email).first()
                if user:
                    # Optional: We could auto-link here, but for now just return user
                    return user
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
            
        user = db.query(User).filter(User.id == auth_provider.user_id).first()
        if not user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
