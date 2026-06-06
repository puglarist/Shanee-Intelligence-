"""Memory management endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException

from shanee.core.memory import MemorySystem, MemoryType

router = APIRouter(prefix="/memory", tags=["memory"])
memory_system = MemorySystem()


@router.post("", status_code=201)
async def store_memory(agent_id: str, memory_type: MemoryType, content: dict):
    """Store a memory entry."""
    entry = memory_system.store_memory(agent_id, memory_type, content)
    return entry.model_dump()


@router.get("/{memory_id}")
async def get_memory(memory_id: str):
    """Retrieve a memory entry."""
    entry = memory_system.retrieve_memory(memory_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Memory not found")
    return entry.model_dump()


@router.get("/agent/{agent_id}")
async def get_agent_memories(agent_id: str, memory_type: Optional[MemoryType] = None):
    """Get all memories for an agent."""
    memories = memory_system.get_agent_memories(agent_id, memory_type)
    return [m.model_dump() for m in memories]


@router.post("/search")
async def search_memories(agent_id: str, query: str):
    """Search memories by keyword."""
    results = memory_system.search_memories(agent_id, query)
    return [m.model_dump() for m in results]
