"""
Base Agent Class
Core agent behavior for all 500 agents in the swarm
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
import asyncio

from huggingface.agent_runtime import AgentContext, AgentAction
from huggingface.inference_router import InferenceRouter
from kernel.dispatcher import Task, TaskType, TaskPriority

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentCapabilities:
    """Capabilities of an agent"""
    max_parallel_tasks: int = 1
    supported_task_types: List[TaskType] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)


class BaseAgent(ABC):
    """
    Base class for all agents in the swarm
    Implements: perception, reasoning, action cycle
    """

    def __init__(
        self,
        agent_id: str,
        role: str,
        domain: str,
        router: InferenceRouter = None
    ):
        self.agent_id = agent_id
        self.role = role
        self.domain = domain
        self.router = router or InferenceRouter()

        # Agent state
        self.context = AgentContext(
            agent_id=agent_id,
            role=role,
            domain=domain
        )
        self.capabilities = AgentCapabilities()
        self.current_task: Optional[Task] = None
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
        self.action_history: List[AgentAction] = []

        # Performance metrics
        self.total_executed = 0
        self.total_successful = 0
        self.total_failed = 0
        self.avg_execution_time = 0.0

        logger.info(f"Initialized {self.__class__.__name__} ({agent_id})")

    @abstractmethod
    async def perceive(self, task: Task) -> str:
        """
        Perception phase: analyze task and environment
        Returns: formatted prompt for inference
        """
        pass

    @abstractmethod
    async def reason(self, perception: str) -> AgentAction:
        """
        Reasoning phase: call HF model to generate reasoning
        Returns: AgentAction with inference result
        """
        pass

    @abstractmethod
    async def act(self, reasoning: AgentAction) -> Dict[str, Any]:
        """
        Action phase: execute the action determined by reasoning
        Returns: result of action execution
        """
        pass

    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """
        Main task execution loop: perceive -> reason -> act
        """
        self.current_task = task
        start_time = datetime.utcnow()

        try:
            logger.info(f"{self.agent_id}: Executing task {task.id}")

            # Phase 1: Perception
            perception = await self.perceive(task)
            logger.debug(f"{self.agent_id}: Perception complete")

            # Phase 2: Reasoning
            reasoning = await self.reason(perception)
            self.action_history.append(reasoning)
            logger.debug(f"{self.agent_id}: Reasoning complete")

            # Phase 3: Action
            result = await self.act(reasoning)
            logger.debug(f"{self.agent_id}: Action complete")

            # Update metrics
            self.total_executed += 1
            self.total_successful += 1
            self.completed_tasks.append(task)

            execution_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_execution_time(execution_time)

            return {
                "status": "success",
                "task_id": task.id,
                "agent_id": self.agent_id,
                "result": result,
                "execution_time": execution_time
            }

        except Exception as e:
            logger.error(f"{self.agent_id}: Task execution failed: {e}")
            self.total_executed += 1
            self.total_failed += 1
            self.failed_tasks.append(task)

            execution_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_execution_time(execution_time)

            return {
                "status": "error",
                "task_id": task.id,
                "agent_id": self.agent_id,
                "error": str(e),
                "execution_time": execution_time
            }

        finally:
            self.current_task = None

    async def execute_batch_tasks(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """Execute multiple tasks sequentially"""
        results = []
        for task in tasks:
            result = await self.execute_task(task)
            results.append(result)
        return results

    def _update_execution_time(self, execution_time: float):
        """Update average execution time"""
        if self.total_executed == 1:
            self.avg_execution_time = execution_time
        else:
            # Exponential moving average
            self.avg_execution_time = (
                (self.avg_execution_time * 0.8) +
                (execution_time * 0.2)
            )

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        success_rate = (
            (self.total_successful / self.total_executed * 100)
            if self.total_executed > 0 else 0
        )

        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "domain": self.domain,
            "current_task": self.current_task.id if self.current_task else None,
            "total_executed": self.total_executed,
            "total_successful": self.total_successful,
            "total_failed": self.total_failed,
            "success_rate": success_rate,
            "avg_execution_time": round(self.avg_execution_time, 3),
            "recent_actions": len(self.action_history)
        }

    def reset_metrics(self):
        """Reset performance metrics"""
        self.total_executed = 0
        self.total_successful = 0
        self.total_failed = 0
        self.avg_execution_time = 0.0
        self.completed_tasks.clear()
        self.failed_tasks.clear()
        self.action_history.clear()


if __name__ == "__main__":
    print("Base agent module - use specific agent implementations")
