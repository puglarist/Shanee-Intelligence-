"""Health check routes."""

from datetime import datetime

from fastapi import APIRouter

from app import __version__
from app.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="ok",
        version=__version__,
        database="connected",
        redis="connected",
        timestamp=datetime.utcnow(),
    )
