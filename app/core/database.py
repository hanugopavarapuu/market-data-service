# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings  # your DB URL lives here

# 1) create the engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,            # if you’re on SQLAlchemy 2.x
)

# 2) configure your Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)
