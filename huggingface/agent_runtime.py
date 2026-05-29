"""
Agent Runtime Environment
Execution context for individual agents to perceive, reason, and act
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio

from .hf_client import HFClient, InferenceRequest, InferenceResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """Execution context for an agent"""
    agent_id: str
    role: str  # "governor" | "domain" | "worker"
    domain: str
    current_task_id: Optional[str] = None
    memory: Dict[str, Any] = None
    environment: Dict[str, Any] = None

    def __post_init__(self):
        if self.memory is None:
            self.memory = {}
        if self.environment is None:
            self.environment = {}


@dataclass
class AgentAction:
    """Action taken by an agent"""
    agent_id: str
    task_id: str
    action_type: str  # "generate", "execute", "validate", "decide"
    payload: Dict[str, Any]
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


class AgentRuntime:
    """
    Runtime environment for executing agents
    Provides perception, inference, action interface
    """

    def __init__(self, hf_client: HFClient = None):
        self.hf_client = hf_client or HFClient()
        self.agents: Dict[str, AgentContext] = {}
        self.execution_log: List[Dict] = []
        self.action_history: List[AgentAction] = []

    def register_agent(self, context: AgentContext) -> bool:
        """Register an agent in the runtime"""
        if context.agent_id in self.agents:
            logger.warning(f"Agent {context.agent_id} already registered")
            return False

        self.agents[context.agent_id] = context
        logger.info(f"Registered agent: {context.agent_id} ({context.role})")
        return True

    async def execute_agent_cycle(
        self,
        agent_id: str,
        task_id: str,
        task_description: str,
        model: str = "meta-llama/Llama-2-70b-chat"
    ) -> AgentAction:
        """
        Execute one perception-inference-action cycle for an agent
        """
        context = self.agents.get(agent_id)
        if not context:
            logger.error(f"Agent {agent_id} not registered")
            return None

        context.current_task_id = task_id

        try:
            # Phase 1: Perception - build prompt from context
            prompt = self._build_perception_prompt(context, task_description)

            # Phase 2: Inference - call HF model
            request = InferenceRequest(
                task_id=task_id,
                agent_id=agent_id,
                model=model,
                prompt=prompt,
                temperature=0.7 if context.role == "governor" else 0.5,
                max_tokens=2048
            )

            response = await self.hf_client.infer(request)

            # Phase 3: Action - process inference result and take action
            action = self._process_inference_result(context, task_id, response)

            # Log execution
            self.action_history.append(action)
            self.execution_log.append({
                "agent_id": agent_id,
                "task_id": task_id,
                "inference_status": response.status,
                "execution_time": response.execution_time,
                "timestamp": datetime.utcnow().isoformat()
            })

            return action

        except Exception as e:
            logger.error(f"Agent {agent_id} cycle failed: {e}")
            return None

    async def execute_batch_cycle(
        self,
        agents: List[str],
        tasks: Dict[str, str]
    ) -> List[AgentAction]:
        """
        Execute parallel cycles for multiple agents
        """
        tasks_to_run = [
            self.execute_agent_cycle(
                agent_id=agent,
                task_id=tasks.get(agent, f"task-{agent}"),
                task_description=f"Task for {agent}",
            )
            for agent in agents if agent in self.agents
        ]

        return await asyncio.gather(*tasks_to_run)

    def _build_perception_prompt(
        self,
        context: AgentContext,
        task_description: str
    ) -> str:
        """Build a prompt from agent perception"""
        role_instructions = {
            "governor": "As a Governor Agent, analyze the current state and generate high-level strategic tasks.",
            "domain": "As a Domain Specialist Agent, execute technical tasks in your domain with precision.",
            "worker": "As a Worker Agent, implement assigned tasks and validate outputs."
        }

        instructions = role_instructions.get(context.role, "")

        prompt = f"""{instructions}

Domain: {context.domain}
Current Task: {task_description}
Agent ID: {context.agent_id}

Memory Context:
{self._format_memory(context.memory)}

Instructions:
1. Analyze the task requirements
2. Consider available knowledge and context
3. Generate a clear, actionable response
4. Include reasoning in your response

Response:"""

        return prompt

    def _format_memory(self, memory: Dict) -> str:
        """Format memory dict into readable string"""
        if not memory:
            return "No previous context"

        lines = []
        for key, value in memory.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)

    def _process_inference_result(
        self,
        context: AgentContext,
        task_id: str,
        response: InferenceResponse
    ) -> AgentAction:
        """Process HF inference result into agent action"""
        action_payload = {
            "inference_output": response.output,
            "status": response.status,
            "tokens_used": response.tokens_used,
            "execution_time": response.execution_time
        }

        # Update agent memory with result
        context.memory[f"task_{task_id}"] = {
            "status": response.status,
            "output_preview": response.output[:100] if response.output else None,
            "timestamp": response.timestamp
        }

        # Determine action type based on agent role and response
        action_type = self._determine_action_type(context.role, response.status)

        action = AgentAction(
            agent_id=context.agent_id,
            task_id=task_id,
            action_type=action_type,
            payload=action_payload
        )

        logger.info(f"Agent {context.agent_id} action: {action_type}")

        return action

    def _determine_action_type(self, role: str, inference_status: str) -> str:
        """Determine action type from role and inference status"""
        if inference_status != "success":
            return "error_handling"

        if role == "governor":
            return "generate"
        elif role == "domain":
            return "execute"
        elif role == "worker":
            return "implement"
        else:
            return "generic"

    def get_agent_status(self, agent_id: str) -> Dict:
        """Get current status of an agent"""
        context = self.agents.get(agent_id)
        if not context:
            return None

        return {
            "agent_id": agent_id,
            "role": context.role,
            "domain": context.domain,
            "current_task": context.current_task_id,
            "memory_size": len(context.memory),
            "recent_actions": [
                {
                    "task_id": a.task_id,
                    "action_type": a.action_type,
                    "timestamp": a.timestamp
                }
                for a in self.action_history[-5:] if a.agent_id == agent_id
            ]
        }

    def get_runtime_stats(self) -> Dict:
        """Get runtime statistics"""
        return {
            "total_agents": len(self.agents),
            "total_executions": len(self.execution_log),
            "successful_executions": sum(
                1 for e in self.execution_log if e.get("inference_status") == "success"
            ),
            "total_actions": len(self.action_history),
            "avg_execution_time": (
                sum(e.get("execution_time", 0) for e in self.execution_log) /
                len(self.execution_log) if self.execution_log else 0
            ),
            "hf_stats": self.hf_client.get_inference_stats()
        }

    def clear_logs(self):
        """Clear execution logs"""
        self.execution_log.clear()
        self.action_history.clear()


if __name__ == "__main__":
    import asyncio

    async def test():
        runtime = AgentRuntime()

        # Register agents
        agents = [
            AgentContext(agent_id="gov-001", role="governor", domain="planning"),
            AgentContext(agent_id="dom-001", role="domain", domain="backend"),
            AgentContext(agent_id="wrk-001", role="worker", domain="implementation"),
        ]

        for agent in agents:
            runtime.register_agent(agent)

        # Execute agent cycles
        print("Executing agent cycles...")
        actions = await runtime.execute_batch_cycle(
            agents=[a.agent_id for a in agents],
            tasks={
                "gov-001": "Generate task list for this sprint",
                "dom-001": "Implement API endpoint validation",
                "wrk-001": "Write unit tests for auth module"
            }
        )

        print(f"\nCompleted {len(actions)} actions")
        for action in actions:
            if action:
                print(f"  {action.agent_id}: {action.action_type}")

        # Show stats
        stats = runtime.get_runtime_stats()
        print(f"\nRuntime Stats: {stats}")

    asyncio.run(test())
