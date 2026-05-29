"""Application configuration and settings."""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "stronghold"
    db_user: str = "stronghold"
    db_password: str = "stronghold_dev_password"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    log_level: str = "info"

    # LLM Configuration
    llm_provider: Literal["claude", "huggingface_local", "huggingface_api"] = (
        "huggingface_local"
    )
    llm_model: str = "mistral-7b-instruct"
    claude_api_key: str = ""
    huggingface_api_key: str = ""

    # Vector DB (Pinecone)
    pinecone_api_key: str = ""
    pinecone_environment: str = "us-west2-az1"
    pinecone_index: str = "stronghold-memories"

    # Security
    secret_key: str = "change-me-in-production"

    # Simulation
    simulation_tick_interval: int = 3600  # seconds
    world_generation_timeout: int = 300  # seconds
    max_concurrent_worlds: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def redis_url(self) -> str:
        """Construct Redis connection URL."""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings()
