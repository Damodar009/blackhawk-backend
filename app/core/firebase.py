import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import get_settings
import os

settings = get_settings()

def get_firebase_app():
    try:
        if not firebase_admin._apps:
            # Check for credentials in standard location or use default
            cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
            
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # Fallback to default credentials (e.g. metadata server on GCP)
                firebase_admin.initialize_app()
        return firebase_admin.get_app()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None
