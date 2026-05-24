"""Agent Runtime - Stateful autonomous intelligence execution"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Callable
from enum import Enum

from pydantic import BaseModel, Field


class AgentState(str, Enum):
    """Agent lifecycle states"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    ERROR = "error"
    STOPPED = "stopped"


@dataclass
class AgentConfig:
    """Configuration for agent creation"""
    name: str
    description: str = ""
    model_id: str = "claude-opus-4-7"
    max_iterations: int = 10
    timeout_seconds: float = 300.0
    enable_memory: bool = True
    enable_tools: bool = True
    system_prompt: Optional[str] = None
    tags: dict[str, str] = field(default_factory=dict)


class Message(BaseModel):
    """Message in agent conversation"""
    role: str = Field(..., description="'user' or 'assistant'")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_use_id: Optional[str] = None
    tool_name: Optional[str] = None


class Perception(BaseModel):
    """What agent perceives from environment"""
    input: str
    context: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Decision(BaseModel):
    """What agent decides to do"""
    action_type: str
    action_params: dict[str, Any] = Field(default_factory=dict)
    reasoning: str = ""


class Action(BaseModel):
    """Executed action result"""
    status: str = "pending"
    result: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class Agent:
    """
    Core agent with perception-action loop.
    Coordinates with models, tools, and memory systems.
    """

    def __init__(self, config: AgentConfig):
        self.id = str(uuid.uuid4())
        self.config = config
        self.state = AgentState.IDLE
        self.created_at = datetime.utcnow()
        self.conversation_history: list[Message] = []
        self.current_iteration = 0

    async def perceive(self, input_text: str) -> Perception:
        """Process sensory input"""
        return Perception(
            input=input_text,
            context={"agent_id": self.id, "iteration": self.current_iteration}
        )

    async def think(self, perception: Perception) -> Decision:
        """Deliberate on action - placeholder for model integration"""
        return Decision(
            action_type="respond",
            action_params={"response": "thinking about: " + perception.input},
            reasoning="Processing input through intelligence core"
        )

    async def act(self, decision: Decision) -> Action:
        """Execute decision"""
        try:
            if decision.action_type == "respond":
                return Action(
                    status="success",
                    result={"response": decision.action_params.get("response")},
                    execution_time_ms=10.0
                )
            else:
                return Action(
                    status="error",
                    error=f"Unknown action type: {decision.action_type}"
                )
        except Exception as e:
            return Action(status="error", error=str(e))

    async def remember(self, message: Message) -> None:
        """Store in conversation memory"""
        self.conversation_history.append(message)

    async def run(self, user_input: str) -> str:
        """Execute one full perception-think-act cycle"""
        self.state = AgentState.THINKING
        self.current_iteration += 1

        try:
            # Store user message
            await self.remember(Message(role="user", content=user_input))

            # Execute cycle
            perception = await self.perceive(user_input)
            decision = await self.think(perception)
            action = await self.act(decision)

            # Store response
            response = str(action.result.get("response")) if action.result else "No response"
            await self.remember(Message(role="assistant", content=response))

            self.state = AgentState.IDLE
            return response

        except Exception as e:
            self.state = AgentState.ERROR
            raise

    def to_dict(self) -> dict:
        """Serialize agent state"""
        return {
            "id": self.id,
            "name": self.config.name,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "iteration": self.current_iteration,
            "history_length": len(self.conversation_history)
        }


class AgentFactory:
    """Factory for creating and managing agents"""

    def __init__(self):
        self.agents: dict[str, Agent] = {}

    def create(self, config: AgentConfig) -> Agent:
        """Create new agent instance"""
        agent = Agent(config)
        self.agents[agent.id] = agent
        return agent

    def get(self, agent_id: str) -> Optional[Agent]:
        """Retrieve agent by ID"""
        return self.agents.get(agent_id)

    def delete(self, agent_id: str) -> bool:
        """Remove agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False

    def list(self) -> list[Agent]:
        """List all agents"""
        return list(self.agents.values())
