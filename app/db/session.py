from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from urllib.parse import quote_plus

from app.core.config import get_settings

import logging

# Setup logger
logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)

# Hide default SQLAlchemy noise
logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)

class DBSession:
    """DB Session.""" 
    def __init__(self):
        settings = get_settings()
        self.engine = create_engine(
            settings.DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
            connect_args={
                'ssl': {'ssl_disabled': True}  # Only if SSL is causing issues
            }
        )

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        try:
            # Best effort "compiled" version
            query = str(statement)
            logger.info("🚀 Executing SQL:\n%s", query)
            logger.info("🔢 Parameters: %s", parameters)
        except Exception as e:
            logger.warning("⚠️ Could not log SQL statement: %s", e)

    @lru_cache
    def create_session(self) -> scoped_session:
        """DB Session Creation."""
        Session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        return Session

    def get_session(self) -> Generator[scoped_session, None, None]:
        """Get DB Session."""
        Session = self.create_session()
        db = Session()
        try:
            yield db
        except Exception as e:
            db.rollback()
            raise  # Let FastAPI handle the error
        finally:
            db.close() 


session = DBSession()
