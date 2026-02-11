from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.auth import FirebaseUser, TokenResponse
from app.models.user import User
from app.models.user_auth_provider import UserAuthProvider
from app.core.firebase import verify_token
from app.core.security import create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid
from datetime import datetime

auth_router = APIRouter()
security = HTTPBearer()

@auth_router.post("/firebase-login", response_model=TokenResponse)
def firebase_login(
    user_data: FirebaseUser,
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(deps.get_db)
):
    # Verify Firebase Token
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    uid = decoded_token.get("uid")
    if uid != user_data.uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token UID does not match provided UID",
        )

    # Check if user exists
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user:
        # Create new user
        new_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            username=user_data.email.split("@")[0] + "_" + str(uuid.uuid4())[:8], # Ensure unique username
            hashed_password="", # No password for social auth
            display_name=user_data.displayName,
            avatar_url=user_data.photoURL,
            is_verified=user_data.emailVerified,
            is_active=True,
            last_login_at=datetime.utcnow()
        )
        db.add(new_user)
        db.flush() # flush to get id
        
        # Add Auth Provider
        # Store Firebase UID as the primary auth provider link
        auth_provider = UserAuthProvider(
            user_id=new_user.id,
            provider="firebase",
            provider_user_id=uid,
            created_at=datetime.utcnow()
        )
        db.add(auth_provider)
        
        # Store original provider data if needed (e.g. google.com)
        # We could add more entries to UserAuthProvider for each provider in user_data.providerData
        for provider in user_data.providerData:
             # Check if we already added this provider (unlikely for new user but good practice)
             if provider.providerId != "firebase":
                 extra_provider = UserAuthProvider(
                     user_id=new_user.id,
                     provider=provider.providerId,
                     provider_user_id=provider.providerUid,
                     created_at=datetime.utcnow()
                 )
                 db.add(extra_provider)
                 
        db.commit()
        db.refresh(new_user)
        user = new_user
    else:
        # User exists, check/update AuthProvider
        auth_provider = db.query(UserAuthProvider).filter(
            UserAuthProvider.user_id == user.id,
            UserAuthProvider.provider == "firebase"
        ).first()
        
        if not auth_provider:
             # Link existing user to firebase
             auth_provider = UserAuthProvider(
                user_id=user.id,
                provider="firebase",
                provider_user_id=uid,
                created_at=datetime.utcnow()
            )
             db.add(auth_provider)
             db.commit()
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        db.add(user)
        db.commit()

    # Create Backend access token
    access_token = create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
