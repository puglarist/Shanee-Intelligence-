"""Main API Server - REST & WebSocket interface for Omniverse OS"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.intelligence import AgentFactory, AgentConfig, ModelConfig, ModelManager

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Request/Response Models
class CreateAgentRequest(BaseModel):
    name: str
    description: str = ""
    model_id: str = "claude-opus-4-7"
    system_prompt: Optional[str] = None


class AgentResponse(BaseModel):
    id: str
    name: str
    state: str
    created_at: str
    history_length: int


class UserMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class AssistantResponse(BaseModel):
    agent_id: str
    response: str
    timestamp: str


# Global state
agent_factory = AgentFactory()
model_config = ModelConfig()
model_manager = ModelManager(model_config)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    logger.info("Starting Shanee Intelligence Omniverse OS")
    yield
    logger.info("Shutting down Shanee Intelligence Omniverse OS")


# Create FastAPI app
app = FastAPI(
    title="Shanee Intelligence Omniverse OS",
    description="Unified intelligence operating system",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """System health status"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "agents": len(agent_factory.list()),
        "model": model_manager.get_model_info()
    }


# Agent Management
@app.post("/agents", response_model=AgentResponse)
async def create_agent(request: CreateAgentRequest):
    """Create new agent"""
    config = AgentConfig(
        name=request.name,
        description=request.description,
        model_id=request.model_id,
        system_prompt=request.system_prompt
    )
    agent = agent_factory.create(config)
    return AgentResponse(
        id=agent.id,
        name=agent.config.name,
        state=agent.state.value,
        created_at=agent.created_at.isoformat(),
        history_length=0
    )


@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get agent details"""
    agent = agent_factory.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return AgentResponse(
        id=agent.id,
        name=agent.config.name,
        state=agent.state.value,
        created_at=agent.created_at.isoformat(),
        history_length=len(agent.conversation_history)
    )


@app.get("/agents", response_model=list[AgentResponse])
async def list_agents():
    """List all agents"""
    agents = agent_factory.list()
    return [
        AgentResponse(
            id=a.id,
            name=a.config.name,
            state=a.state.value,
            created_at=a.created_at.isoformat(),
            history_length=len(a.conversation_history)
        )
        for a in agents
    ]


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete agent"""
    if not agent_factory.delete(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted"}


# Agent Interaction
@app.post("/agents/{agent_id}/message", response_model=AssistantResponse)
async def send_message(agent_id: str, request: UserMessageRequest):
    """Send message to agent"""
    agent = agent_factory.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        response = await agent.run(request.message)
        return AssistantResponse(
            agent_id=agent_id,
            response=response,
            timestamp=agent.conversation_history[-1].timestamp.isoformat()
        )
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# System
@app.get("/status")
async def system_status():
    """Get system status"""
    return {
        "system": "Shanee Intelligence Omniverse OS",
        "version": "0.1.0",
        "agents_active": len(agent_factory.list()),
        "model_provider": model_manager.config.provider.value,
        "model_id": model_manager.config.model_id,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
