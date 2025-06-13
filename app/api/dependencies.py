# app/api/dependencies.py
from typing import Generator
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal  # wherever you defined SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
