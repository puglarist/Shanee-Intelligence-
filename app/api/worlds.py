"""World generation and management routes."""

import uuid
from datetime import datetime

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import World, WorldType
from app.schemas import WorldCreateRequest, WorldResponse

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post("/worlds/generate", response_model=WorldResponse, status_code=201)
async def create_world(
    request: WorldCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Create and begin generating a new world.

    This endpoint initiates world generation with the specified parameters.
    The world will be generated asynchronously.
    """
    try:
        world_id = f"world_{uuid.uuid4().hex[:12]}"

        world = World(
            id=world_id,
            name=request.name,
            world_type=WorldType[request.world_type.upper()],
            seed=request.generation_params.world_seed or int.from_bytes(
                uuid.uuid4().bytes, "big"
            ) % (2**31),
            generation_params=request.generation_params.model_dump(),
            generation_status="pending",
        )

        db.add(world)
        await db.commit()
        await db.refresh(world)

        logger.info(
            "World creation initiated",
            world_id=world_id,
            world_name=request.name,
        )

        return WorldResponse.model_validate(world)

    except Exception as e:
        await db.rollback()
        logger.error(
            "World creation failed",
            error=str(e),
            request=request.model_dump(),
        )
        raise HTTPException(status_code=500, detail="Failed to create world")


@router.get("/worlds/{world_id}", response_model=WorldResponse)
async def get_world(
    world_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve world metadata and status.

    Returns information about a specific world including generation status
    and basic statistics.
    """
    from sqlalchemy import select

    result = await db.execute(select(World).filter(World.id == world_id))
    world = result.scalar_one_or_none()

    if not world:
        raise HTTPException(status_code=404, detail="World not found")

    return WorldResponse.model_validate(world)


@router.get("/worlds", response_model=list[WorldResponse])
async def list_worlds(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    List all worlds.

    Returns a paginated list of all generated worlds.
    """
    from sqlalchemy import select

    result = await db.execute(
        select(World).offset(skip).limit(limit).order_by(World.created_at.desc())
    )
    worlds = result.scalars().all()

    return [WorldResponse.model_validate(world) for world in worlds]
