"""Core Agent class for Shanee Intelligence."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Agent execution status."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"


class AgentConfig(BaseModel):
    """Agent configuration."""
    name: str
    description: str = ""
    max_iterations: int = 10
    timeout_seconds: int = 300
    tools: List[str] = Field(default_factory=list)
    memory_enabled: bool = True
    enable_logging: bool = True


class Agent(BaseModel):
    """Core Agent class."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    config: AgentConfig
    status: AgentStatus = AgentStatus.IDLE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    context: Dict[str, Any] = Field(default_factory=dict)
    execution_history: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        use_enum_values = False

    def update_status(self, status: AgentStatus) -> None:
        """Update agent status."""
        self.status = status
        self.last_activity = datetime.utcnow()

    def add_to_history(self, event: Dict[str, Any]) -> None:
        """Add execution event to history."""
        self.execution_history.append({
            **event,
            "timestamp": datetime.utcnow()
        })

    def get_context(self, key: str) -> Any:
        """Get context value."""
        return self.context.get(key)

    def set_context(self, key: str, value: Any) -> None:
        """Set context value."""
        self.context[key] = value
        self.last_activity = datetime.utcnow()
