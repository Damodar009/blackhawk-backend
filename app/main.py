from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import get_routers
from app.core.config import get_settings
from app.core.logging import setup_logging

# Setup logging first
setup_logging()

class App:

    """Entry Point."""

    settings = get_settings()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION
    )

    def add_cors(self):
        """Add cors method."""

        origins = self.settings.BACKEND_CORS_ORIGINS
        self.app.add_middleware(
            CORSMiddleware, 
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def add_health_check(self):
        """Add health check"""
        @self.app.get("/health-check", tags=["Health"])
        def health_check():
            return {"message": "API up and running"}


    def start_application(self) -> FastAPI:
        """Start application method."""

        get_routers(self.app)
        self.add_cors()
        self.add_health_check()

        return self.app


app = App().start_application()
