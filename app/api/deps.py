from typing import Generator
from app.db.session import session

def get_db() -> Generator:
    yield from session.get_session()
