from functools import lru_cache
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = f"FELIX IT API"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str
    
    model_config = SettingsConfigDict(
        env_file=".env"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()