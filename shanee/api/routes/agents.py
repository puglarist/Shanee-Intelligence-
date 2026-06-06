"""Agent management endpoints."""

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from shanee.core.agents import AgentManager, AgentConfig

router = APIRouter(prefix="/agents", tags=["agents"])
manager = AgentManager()


@router.post("", status_code=201)
async def create_agent(config: AgentConfig):
    """Create a new agent."""
    agent = manager.create_agent(config)
    return agent.model_dump()


@router.get("")
async def list_agents(status: Optional[str] = None):
    """List all agents."""
    agents = manager.list_agents()
    return [a.model_dump() for a in agents]


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details."""
    agent = manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.model_dump()


@router.delete("/{agent_id}", status_code=204)
async def terminate_agent(agent_id: str):
    """Terminate an agent."""
    if not manager.terminate_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return None
