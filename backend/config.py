from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    api_title: str = "Shanee Intelligence API"
    api_version: str = "0.1.0"
    debug: bool = True

    # Security
    secret_key: str  # Required - must be set via environment variable
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database (PostgreSQL - optional for MVP)
    database_url: Optional[str] = None

    # GPU Configuration
    runpod_api_key: Optional[str] = None
    enable_gpu: bool = False

    # Storage Configuration
    storage_backend: str = "local"  # local, s3, github
    github_token: Optional[str] = None

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
