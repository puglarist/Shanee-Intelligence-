"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Shanee Intelligence API",
        description="Multi-agent orchestration platform",
        version="0.2.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routes.health.router)
    app.include_router(routes.agents.router)
    app.include_router(routes.memory.router)
    app.include_router(routes.tools.router)

    return app
