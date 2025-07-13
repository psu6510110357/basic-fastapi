import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL_PG: str = os.getenv("DATABASE_URL_PG") or "sqlite+aiosqlite:///database.db"
    SECRET_KEY: str = "secret"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5 * 60  # 5 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    model_config = {"env_file": ".env", "validate_assignment": True, "extra": "allow"}


def get_settings():
    return Settings()
