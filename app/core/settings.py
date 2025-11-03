# app/core/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # JWT / security
    SECRET_KEY: str = "change-this-in-dev"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # Database
    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "app"
    POSTGRES_DB: str = "splitwise"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # Full SQLAlchemy URL used by your Session engine
    DATABASE_URL: str = "postgresql+psycopg2://app:app@db:5432/splitwise"

    # Optional env marker
    ENV: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
