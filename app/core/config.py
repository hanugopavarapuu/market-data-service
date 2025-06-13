# app/core/config.py
import os
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    database_url: AnyUrl
    alpha_vantage_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Then elsewhere when creating your engine:
from sqlalchemy import create_engine
engine = create_engine(settings.database_url)
