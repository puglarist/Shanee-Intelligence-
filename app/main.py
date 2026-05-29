"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from datetime import datetime

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api import health, worlds
from app.config import settings
from app.schemas import HealthResponse

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown logic."""
    # Startup
    logger.info("Starting Stronghold Genesis AI", version=__version__)
    yield
    # Shutdown
    logger.info("Shutting down Stronghold Genesis AI")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Stronghold Genesis AI",
        description="Autonomous AI Omniverse World Generation System",
        version=__version__,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        return HealthResponse(
            status="ok",
            version=__version__,
            database="connected",
            redis="connected",
            timestamp=datetime.utcnow(),
        )

    # Include routers
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(worlds.router, prefix="/api", tags=["worlds"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level,
    )
