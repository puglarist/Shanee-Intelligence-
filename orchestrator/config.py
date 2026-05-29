"""Configuration module for Omniverse Engine orchestrator.

This module reads configuration ONLY from environment variables.
No secrets are stored in code or logs.
"""
import os
import sys
from typing import Optional


class Config:
    """Configuration for the orchestrator."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        self.hf_api_key: Optional[str] = os.getenv("HF_API_KEY")
        self.hf_model_endpoint: Optional[str] = os.getenv("HF_MODEL_ENDPOINT")
        self.database_url: Optional[str] = os.getenv("DATABASE_URL")
        self.mock_mode: bool = self.hf_api_key == "mock"
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.port: int = int(os.getenv("PORT", "8000"))
        self.host: str = os.getenv("HOST", "0.0.0.0")

    def validate(self) -> None:
        """Validate configuration.

        In production mode (not mock), HF_API_KEY must be set.
        Exit with error if validation fails.
        """
        if not self.mock_mode and not self.hf_api_key:
            print(
                "ERROR: HF_API_KEY environment variable not set and not in mock mode.",
                file=sys.stderr,
            )
            print("Set HF_API_KEY or HF_API_KEY=mock for local testing.", file=sys.stderr)
            sys.exit(1)

        if not self.hf_model_endpoint and not self.mock_mode:
            print(
                "WARNING: HF_MODEL_ENDPOINT not set. Using default Hugging Face endpoint.",
                file=sys.stderr,
            )

    def __repr__(self) -> str:
        """Return string representation without exposing secrets."""
        return (
            f"Config(mock_mode={self.mock_mode}, "
            f"has_hf_key={bool(self.hf_api_key)}, "
            f"has_endpoint={bool(self.hf_model_endpoint)}, "
            f"debug={self.debug})"
        )


# Global configuration instance
config = Config()
