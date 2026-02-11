from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class Metadata(BaseModel):
    creationTime: Optional[str] = None
    lastSignInTime: Optional[str] = None

class ProviderData(BaseModel):
    providerId: str
    providerUid: str
    displayName: Optional[str] = None
    email: Optional[str] = None
    photoURL: Optional[str] = None
    phoneNumber: Optional[str] = None

class FirebaseUser(BaseModel):
    uid: str
    email: Optional[str] = None
    emailVerified: bool = False
    displayName: Optional[str] = None
    phoneNumber: Optional[str] = None
    photoURL: Optional[str] = None
    isAnonymous: bool = False
    providerData: List[ProviderData] = []
    metadata: Optional[Metadata] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
