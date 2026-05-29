"""
Agent Registry
Manages lifecycle and coordination of 500-agent swarm
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import uuid
from datetime import datetime
import json
from pathlib import Path

class AgentStatus(Enum):
    """Agent lifecycle states"""
    IDLE = "idle"
    BUSY = "busy"
    WAITING = "waiting"
    ERROR = "error"
    TERMINATED = "terminated"

@dataclass
class AgentMetrics:
    """Performance metrics for an agent"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    avg_execution_time: float = 0.0
    last_execution: Optional[str] = None
    success_rate: float = 0.0

@dataclass
class AgentState:
    """Current state of an agent"""
    agent_id: str
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[str] = None
    metrics: AgentMetrics = field(default_factory=AgentMetrics)
    last_heartbeat: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    error_message: Optional[str] = None

class AgentRegistry:
    """
    Central registry managing all 500 agents
    Handles: spawning, lifecycle, coordination, monitoring
    """

    def __init__(self, config=None):
        self.config = config
        self.agents: Dict[str, AgentState] = {}
        self.agents_by_role: Dict[str, List[str]] = {
            "governor": [],
            "domain": [],
            "worker": []
        }
        self.agents_by_domain: Dict[str, List[str]] = {}
        self.load_registry()

    def spawn_agent(self, role: str, domain: str, agent_id: Optional[str] = None) -> str:
        """
        Spawn a new agent
        Returns: agent_id
        """
        if agent_id is None:
            agent_id = f"{role[:3]}-{domain[:3]}-{str(uuid.uuid4())[:8]}"

        agent_state = AgentState(agent_id=agent_id)
        self.agents[agent_id] = agent_state

        # Register by role
        if role not in self.agents_by_role:
            self.agents_by_role[role] = []
        self.agents_by_role[role].append(agent_id)

        # Register by domain
        if domain not in self.agents_by_domain:
            self.agents_by_domain[domain] = []
        self.agents_by_domain[domain].append(agent_id)

        return agent_id

    def spawn_swarm(self, config) -> Dict[str, List[str]]:
        """
        Spawn the entire 500-agent swarm based on config
        Returns: mapping of agents by role
        """
        spawned = {"governor": [], "domain": [], "worker": []}

        # Spawn governor agents (20)
        for i in range(config.governor_agents):
            agent_id = self.spawn_agent("governor", f"gov-{i}")
            spawned["governor"].append(agent_id)

        # Spawn domain agents (300)
        domains = [
            "unreal_engine", "backend", "ai_generation", "multiplayer",
            "swift_ios", "cinematics", "security", "networking"
        ]
        domain_count = config.domain_agents // len(domains)
        for domain in domains:
            for i in range(domain_count):
                agent_id = self.spawn_agent("domain", domain)
                spawned["domain"].append(agent_id)

        # Spawn worker agents (180)
        for i in range(config.worker_agents):
            agent_id = self.spawn_agent("worker", f"work-{i}")
            spawned["worker"].append(agent_id)

        return spawned

    def get_agent(self, agent_id: str) -> Optional[AgentState]:
        """Get agent by ID"""
        return self.agents.get(agent_id)

    def update_agent_status(self, agent_id: str, status: AgentStatus, task_id: Optional[str] = None):
        """Update agent status"""
        if agent_id in self.agents:
            self.agents[agent_id].status = status
            self.agents[agent_id].current_task = task_id
            self.agents[agent_id].last_heartbeat = datetime.utcnow().isoformat()

    def get_agents_by_role(self, role: str) -> List[AgentState]:
        """Get all agents of a specific role"""
        return [self.agents[aid] for aid in self.agents_by_role.get(role, [])]

    def get_agents_by_domain(self, domain: str) -> List[AgentState]:
        """Get all agents in a specific domain"""
        return [self.agents[aid] for aid in self.agents_by_domain.get(domain, [])]

    def get_idle_agents(self, count: int = 1) -> List[AgentState]:
        """Get idle agents available for work"""
        idle = [state for state in self.agents.values() if state.status == AgentStatus.IDLE]
        return idle[:count]

    def get_swarm_health(self) -> Dict:
        """Get health metrics for entire swarm"""
        total = len(self.agents)
        idle = sum(1 for s in self.agents.values() if s.status == AgentStatus.IDLE)
        busy = sum(1 for s in self.agents.values() if s.status == AgentStatus.BUSY)
        error = sum(1 for s in self.agents.values() if s.status == AgentStatus.ERROR)

        avg_success_rate = sum(s.metrics.success_rate for s in self.agents.values()) / total if total > 0 else 0
        total_tasks = sum(s.metrics.total_tasks for s in self.agents.values())

        return {
            "total_agents": total,
            "idle": idle,
            "busy": busy,
            "error": error,
            "total_tasks_completed": total_tasks,
            "avg_success_rate": avg_success_rate,
            "timestamp": datetime.utcnow().isoformat()
        }

    def save_registry(self, path: str = "registry.json"):
        """Save registry to disk"""
        data = {
            "agents": {
                agent_id: {
                    "status": state.status.value,
                    "current_task": state.current_task,
                    "metrics": {
                        "total_tasks": state.metrics.total_tasks,
                        "completed_tasks": state.metrics.completed_tasks,
                        "failed_tasks": state.metrics.failed_tasks,
                        "success_rate": state.metrics.success_rate
                    }
                }
                for agent_id, state in self.agents.items()
            },
            "health": self.get_swarm_health()
        }

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_registry(self, path: str = "registry.json"):
        """Load registry from disk"""
        p = Path(path)
        if p.exists():
            with open(path) as f:
                data = json.load(f)
                # Restore agents (simplified - full impl would restore state)
                for agent_id in data.get("agents", {}):
                    if agent_id not in self.agents:
                        role = agent_id.split('-')[0]
                        domain = agent_id.split('-')[1]
                        self.spawn_agent(role, domain, agent_id)

    def get_agent_by_specialization(self, specialization: str) -> List[AgentState]:
        """Get agents by specialization (e.g., 'code', 'test', 'debug')"""
        # This will be expanded as agent specializations are defined
        return []

    def terminate_agent(self, agent_id: str):
        """Terminate an agent"""
        if agent_id in self.agents:
            self.agents[agent_id].status = AgentStatus.TERMINATED

    def get_total_agent_count(self) -> int:
        """Get total number of agents"""
        return len(self.agents)

if __name__ == "__main__":
    from config import SwarmConfig, ConfigManager

    config = ConfigManager()
    registry = AgentRegistry(config)

    # Spawn swarm
    print("Spawning 500-agent swarm...")
    spawned = registry.spawn_swarm(config.swarm_config)

    print(f"Governor agents: {len(spawned['governor'])}")
    print(f"Domain agents: {len(spawned['domain'])}")
    print(f"Worker agents: {len(spawned['worker'])}")
    print(f"Total agents: {registry.get_total_agent_count()}")

    # Show health
    health = registry.get_swarm_health()
    print(f"\nSwarm Health: {health}")
