"""FastAPI orchestration engine for the Omniverse Engine.

Provides REST API endpoints for:
- Health checks
- Executing swarm cycles
- Listing and managing agents
- Managing tasks
"""
import sys
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

from orchestrator.agents import list_agent_roles, count_agents, get_agent_role
from orchestrator.config import config
from orchestrator.hf_client import hf_client
from orchestrator.tasks import queue, Task

# Validate configuration on startup
config.validate()

# Create FastAPI app
app = FastAPI(
    title="Omniverse Engine Orchestrator",
    description="Distributed AI swarm orchestration for world simulation",
    version="1.0.0",
)


# Request/Response models
class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    timestamp: str
    mode: str
    agents_count: int
    config: Dict[str, Any]


class AgentInfo(BaseModel):
    """Agent information."""

    name: str
    description: str
    capabilities: List[str]
    priority: int


class TaskInfo(BaseModel):
    """Task information."""

    id: str
    agent_id: str
    agent_role: str
    task_type: str
    status: str
    created_at: str
    updated_at: str


class ExecuteRequest(BaseModel):
    """Request to execute a swarm cycle."""

    agent_role: str
    task_type: str
    payload: Dict[str, Any]


class ExecuteResponse(BaseModel):
    """Response from swarm cycle execution."""

    status: str
    task_id: str
    message: str


# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        Health status and configuration information
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        mode="mock" if config.mock_mode else "production",
        agents_count=count_agents(),
        config={
            "mock_mode": config.mock_mode,
            "has_hf_key": bool(config.hf_api_key and config.hf_api_key != "mock"),
            "has_endpoint": bool(config.hf_model_endpoint),
            "debug": config.debug,
        },
    )


@app.get("/agents", response_model=List[AgentInfo])
async def list_agents() -> List[AgentInfo]:
    """List all available agent roles.

    Returns:
        List of available agents
    """
    return [
        AgentInfo(
            name=role.name,
            description=role.description,
            capabilities=role.capabilities,
            priority=role.priority,
        )
        for role in list_agent_roles()
    ]


@app.get("/agents/{agent_name}")
async def get_agent(agent_name: str) -> Dict[str, Any]:
    """Get details for a specific agent.

    Args:
        agent_name: Name of the agent to retrieve

    Returns:
        Agent details or 404 if not found
    """
    role = get_agent_role(agent_name)
    if not role:
        return {"error": f"Agent '{agent_name}' not found"}

    return {
        "name": role.name,
        "description": role.description,
        "capabilities": role.capabilities,
        "priority": role.priority,
    }


@app.get("/tasks", response_model=Dict[str, Any])
async def get_tasks() -> Dict[str, Any]:
    """Get pending tasks.

    Returns:
        Dictionary with task statistics and pending tasks
    """
    stats = queue.stats()
    return {
        "stats": stats,
        "pending": [
            TaskInfo(
                id=task.id,
                agent_id=task.agent_id,
                agent_role=task.agent_role,
                task_type=task.task_type,
                status=task.status,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in queue.get_pending_tasks()
        ],
    }


@app.post("/execute", response_model=ExecuteResponse)
async def execute_swarm_cycle(request: ExecuteRequest) -> ExecuteResponse:
    """Execute a swarm cycle.

    Args:
        request: Execution request with agent role and task

    Returns:
        Response with task ID and status
    """
    # Verify agent exists
    role = get_agent_role(request.agent_role)
    if not role:
        return ExecuteResponse(
            status="error",
            task_id="",
            message=f"Agent role '{request.agent_role}' not found",
        )

    # Create task in queue
    task = queue.enqueue(
        agent_id=f"{request.agent_role}_{datetime.utcnow().timestamp()}",
        agent_role=request.agent_role,
        task_type=request.task_type,
        payload=request.payload,
    )

    return ExecuteResponse(
        status="enqueued",
        task_id=task.id,
        message=f"Task created for agent '{request.agent_role}' with type '{request.task_type}'",
    )


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get status of a specific task.

    Args:
        task_id: ID of the task

    Returns:
        Task details or 404 if not found
    """
    task = queue.get_task(task_id)
    if not task:
        return {"error": f"Task '{task_id}' not found"}

    return {
        "id": task.id,
        "agent_id": task.agent_id,
        "agent_role": task.agent_role,
        "task_type": task.task_type,
        "status": task.status,
        "result": task.result,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


@app.get("/stats")
async def get_stats() -> Dict[str, Any]:
    """Get overall system statistics.

    Returns:
        System statistics
    """
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "agents": count_agents(),
        "tasks": queue.stats(),
        "mode": "mock" if config.mock_mode else "production",
    }


def main():
    """Main entry point for the orchestrator."""
    import uvicorn

    print(f"Starting Omniverse Engine Orchestrator: {config}")
    print(f"  Agents: {count_agents()}")
    print(f"  Mock mode: {config.mock_mode}")
    print(f"  Server: {config.host}:{config.port}")

    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info" if config.debug else "warning",
    )


if __name__ == "__main__":
    main()
