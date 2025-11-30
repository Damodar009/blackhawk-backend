import os
from functools import lru_cache
from pathlib import Path
from typing import List
from urllib.parse import quote_plus

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application Settings with dynamic DATABASE_URL construction."""

    def __init__(self):
        # Project
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Blackhawk Backend")
        self.PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        
        # Database Configuration
        self.DB_USER: str = os.getenv("DB_USER", "root")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD", "secret")
        self.DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
        self.DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
        self.DB_NAME: str = os.getenv("DB_NAME", "blackhawk")
        
        # Construct DATABASE_URL with encoded password
        self.DATABASE_URL: str = self._build_database_url()
        
        # Security
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "somesecretkey")
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        
        # AI Services
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        self.HUGGINGFACEHUB_API_TOKEN: str = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
        
        # API Configuration
        self.API_V1_STR: str = "/api/v1"
        
        # CORS
        cors_origins = os.getenv("BACKEND_CORS_ORIGINS", "")
        if cors_origins:
            self.BACKEND_CORS_ORIGINS: List[str] = [
                origin.strip() for origin in cors_origins.split(",")
            ]
        else:
            self.BACKEND_CORS_ORIGINS: List[str] = [
                "http://localhost:3000",
                "http://localhost:8000",
                "http://localhost:5173",
            ]
        
        # Database Pool Settings
        self.DB_POOL_SIZE: int = 5
        self.DB_MAX_OVERFLOW: int = 10
        self.DB_POOL_RECYCLE: int = 3600
        self.DB_POOL_PRE_PING: bool = True
        
        # Debug print (only in development)
        if self.ENVIRONMENT == "development":
            self._print_debug_info()
    
    def _build_database_url(self) -> str:
        """Build DATABASE_URL with properly encoded password."""
        # URL encode password to handle special characters like @, #, %, etc.
        encoded_password = quote_plus(self.DB_PASSWORD)
        
        # Construct the database URL
        url = (
            f"mysql+pymysql://{self.DB_USER}:{encoded_password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return url
    
    def _print_debug_info(self):
        """Print debug information (only in development)."""
        print("\n" + "="*50)
        print("🔧 Application Configuration")
        print("="*50)
        print(f"📦 Project: {self.PROJECT_NAME} v{self.PROJECT_VERSION}")
        print(f"🌍 Environment: {self.ENVIRONMENT}")
        print(f"🗄️  Database: {self.DB_NAME}")
        print(f"🔗 Host: {self.DB_HOST}:{self.DB_PORT}")
        print(f"👤 User: {self.DB_USER}")
        print(f"🔐 Password: {self.DB_PASSWORD}")
        print("="*50 + "\n")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create global settings instance
settings = get_settings()