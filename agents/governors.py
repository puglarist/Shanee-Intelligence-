"""
Governor Agents
Strategic planning and task generation for the swarm
20 governors across 8 domains make high-level decisions and generate tasks
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

from .base import BaseAgent, AgentCapabilities
from kernel.dispatcher import Task, TaskType, TaskPriority
from huggingface.agent_runtime import AgentAction
from huggingface.inference_router import InferenceRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GovernorAgent(BaseAgent):
    """
    Governor Agent - High-level strategic agent
    Responsibilities:
    - Analyze swarm state and repository state
    - Generate strategic tasks for domain agents
    - Coordinate cross-domain initiatives
    - Manage resource allocation
    """

    def __init__(self, agent_id: str, domain: str, router: InferenceRouter = None):
        super().__init__(agent_id=agent_id, role="governor", domain=domain, router=router)

        # Governor-specific capabilities
        self.capabilities = AgentCapabilities(
            max_parallel_tasks=3,
            supported_task_types=[
                TaskType.ARCHITECTURE,
                TaskType.RESEARCH,
                TaskType.CODE_GENERATION,
            ],
            domains=[domain],
            specializations=["planning", "coordination", "task_generation"]
        )

        # State monitoring
        self.last_analysis: Dict = {}
        self.task_generation_history: List[Task] = []
        self.strategy_log: List[Dict] = []

    async def perceive(self, task: Task) -> str:
        """
        Governor perception: analyze system state and repository
        Focus on: architecture, improvements, strategic needs
        """
        # In real system, would read from repo/memory
        perception = f"""
Governor Agent Perception Report
Agent: {self.agent_id}
Domain: {self.domain}
Task: {task.description}

Current Focus Areas:
1. System Architecture - Review current design patterns
2. Code Quality - Identify technical debt
3. Performance - Monitor execution metrics
4. Documentation - Ensure clarity for team

Repository State:
- Total commits this session: [to be read from repo]
- Active agent count: [to be tracked by orchestrator]
- Task completion rate: [to be calculated by dispatcher]

Task Objective:
{task.description}

Analysis Request:
Provide strategic insights, identify improvement opportunities, and suggest new tasks for domain agents.
Consider: architecture improvements, code patterns, cross-domain coordination needs.
"""
        return perception

    async def reason(self, perception: str) -> AgentAction:
        """
        Governor reasoning: use HF model to generate strategic analysis and tasks
        """
        try:
            response = await self.router.execute_routed_request(
                task_id=self.current_task.id if self.current_task else "reasoning",
                agent_id=self.agent_id,
                task_type="analysis",
                prompt=perception
            )

            action = AgentAction(
                agent_id=self.agent_id,
                task_id=self.current_task.id if self.current_task else "reasoning",
                action_type="generate",
                payload={
                    "analysis": response.output,
                    "status": response.status,
                    "execution_time": response.execution_time
                }
            )

            return action

        except Exception as e:
            logger.error(f"Governor {self.agent_id} reasoning failed: {e}")
            raise

    async def act(self, reasoning: AgentAction) -> Dict[str, Any]:
        """
        Governor action: parse reasoning and generate tasks
        """
        try:
            analysis = reasoning.payload.get("analysis", "")

            # Parse analysis to extract suggested tasks
            generated_tasks = self._parse_task_suggestions(analysis)

            # Log strategy decision
            self.strategy_log.append({
                "timestamp": datetime.utcnow().isoformat(),
                "analysis_summary": analysis[:200],
                "tasks_generated": len(generated_tasks)
            })

            return {
                "tasks_generated": len(generated_tasks),
                "tasks": [
                    {
                        "id": t.id,
                        "type": t.type.value,
                        "priority": t.priority.value,
                        "title": t.title
                    }
                    for t in generated_tasks
                ],
                "strategy_notes": self._extract_strategy_notes(analysis)
            }

        except Exception as e:
            logger.error(f"Governor {self.agent_id} action failed: {e}")
            raise

    def _parse_task_suggestions(self, analysis: str) -> List[Task]:
        """
        Parse governor analysis to extract task suggestions
        In real system, would use NLP to parse structured tasks
        """
        # For now, generate example tasks based on analysis content
        tasks = []

        suggested_types = [
            (TaskType.CODE_GENERATION, "Generate"),
            (TaskType.TESTING, "Test"),
            (TaskType.DEBUGGING, "Debug"),
            (TaskType.DOCUMENTATION, "Document"),
        ]

        task_count = 0
        for task_type, action in suggested_types:
            if action.lower() in analysis.lower():
                task = Task(
                    id=f"{self.agent_id}-gen-{task_count}",
                    type=task_type,
                    priority=TaskPriority.MEDIUM,
                    title=f"{action} for {self.domain}",
                    description=f"Generated task by {self.agent_id}",
                    required_domain=self.domain
                )
                tasks.append(task)
                task_count += 1

        # Always generate at least one task
        if not tasks:
            task = Task(
                id=f"{self.agent_id}-gen-default",
                type=TaskType.CODE_GENERATION,
                priority=TaskPriority.MEDIUM,
                title=f"Implement improvements in {self.domain}",
                description=f"Strategic improvement task generated by {self.agent_id}",
                required_domain=self.domain
            )
            tasks.append(task)

        self.task_generation_history.extend(tasks)
        return tasks

    def _extract_strategy_notes(self, analysis: str) -> str:
        """Extract key strategy notes from analysis"""
        lines = analysis.split('\n')
        notes = [line.strip() for line in lines if line.strip() and len(line.strip()) > 20]
        return '\n'.join(notes[:3])  # Top 3 notes

    def get_governor_status(self) -> Dict[str, Any]:
        """Get detailed governor status"""
        status = self.get_status()
        status.update({
            "tasks_generated": len(self.task_generation_history),
            "strategies_executed": len(self.strategy_log),
            "domain_expertise": self.domain,
            "recent_strategies": self.strategy_log[-3:] if self.strategy_log else []
        })
        return status

    def reset_generation_history(self):
        """Reset task generation history"""
        self.task_generation_history.clear()
        self.strategy_log.clear()


async def create_governor_swarm(
    count: int = 20,
    domains: List[str] = None,
    router: InferenceRouter = None
) -> List[GovernorAgent]:
    """
    Create a swarm of governor agents
    """
    if domains is None:
        domains = [
            "unreal_engine", "backend", "ai_generation", "multiplayer",
            "swift_ios", "cinematics", "security", "networking"
        ]

    governors = []
    agents_per_domain = count // len(domains)

    for domain_idx, domain in enumerate(domains):
        for agent_idx in range(agents_per_domain):
            agent_id = f"gov-{domain[:3]}-{agent_idx:02d}"
            governor = GovernorAgent(
                agent_id=agent_id,
                domain=domain,
                router=router
            )
            governors.append(governor)

    logger.info(f"Created {len(governors)} governor agents across {len(domains)} domains")
    return governors


if __name__ == "__main__":
    asyncio.run(create_governor_swarm(count=4))
