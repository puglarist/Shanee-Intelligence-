"""
Swarm Lifecycle Manager
Manages initialization, health monitoring, and recovery of 500-agent swarm
Ensures continuous 24/7 logical operation
"""

import logging
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentHealthStatus(Enum):
    """Agent health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    IDLE = "idle"
    RECOVERING = "recovering"


@dataclass
class AgentHealthMetrics:
    """Health metrics for an agent"""
    agent_id: str
    status: AgentHealthStatus
    last_heartbeat: str
    tasks_completed: int = 0
    failure_count: int = 0
    response_time_ms: float = 0.0
    is_idle_too_long: bool = False
    recovery_attempts: int = 0


@dataclass
class SwarmHealthSnapshot:
    """Health snapshot of entire swarm"""
    timestamp: str
    total_agents: int
    healthy_agents: int
    degraded_agents: int
    failed_agents: int
    idle_agents: int
    overall_health_score: float
    avg_response_time: float
    task_throughput: float


class SwarmLifecycleManager:
    """
    Manages agent lifecycle for 500-agent swarm
    Handles: initialization, monitoring, recovery, rebalancing
    """

    def __init__(self):
        self.agent_metrics: Dict[str, AgentHealthMetrics] = {}
        self.swarm_state = "initializing"  # initializing -> running -> paused -> error
        self.health_history: List[SwarmHealthSnapshot] = []
        self.idle_threshold_seconds = 300  # 5 minutes
        self.recovery_max_attempts = 3
        self.last_health_check = datetime.utcnow()

    def register_agent(self, agent_id: str) -> bool:
        """Register an agent in the lifecycle manager"""
        if agent_id in self.agent_metrics:
            return False

        self.agent_metrics[agent_id] = AgentHealthMetrics(
            agent_id=agent_id,
            status=AgentHealthStatus.HEALTHY,
            last_heartbeat=datetime.utcnow().isoformat()
        )
        logger.info(f"Registered agent {agent_id} in lifecycle manager")
        return True

    async def register_agent_batch(self, agent_ids: List[str]) -> int:
        """Register multiple agents"""
        count = 0
        for agent_id in agent_ids:
            if self.register_agent(agent_id):
                count += 1
        logger.info(f"Registered {count} agents in batch")
        return count

    def update_agent_heartbeat(self, agent_id: str, response_time_ms: float = 0.0):
        """Update agent heartbeat on activity"""
        if agent_id in self.agent_metrics:
            metrics = self.agent_metrics[agent_id]
            metrics.last_heartbeat = datetime.utcnow().isoformat()
            metrics.response_time_ms = response_time_ms
            metrics.is_idle_too_long = False

    def mark_task_completed(self, agent_id: str):
        """Record task completion for agent"""
        if agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].tasks_completed += 1

    def mark_task_failed(self, agent_id: str):
        """Record task failure for agent"""
        if agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].failure_count += 1

    def get_agent_status(self, agent_id: str) -> Optional[AgentHealthMetrics]:
        """Get current status of an agent"""
        return self.agent_metrics.get(agent_id)

    async def check_swarm_health(self) -> SwarmHealthSnapshot:
        """
        Check health of entire swarm
        Detects idle agents, failed agents, and degraded performance
        """
        now = datetime.utcnow()
        healthy = 0
        degraded = 0
        failed = 0
        idle = 0

        # Check each agent
        for agent_id, metrics in self.agent_metrics.items():
            last_heartbeat = datetime.fromisoformat(metrics.last_heartbeat)
            idle_duration = (now - last_heartbeat).total_seconds()

            # Determine status
            if metrics.failure_count > 5:
                metrics.status = AgentHealthStatus.FAILED
                failed += 1
            elif idle_duration > self.idle_threshold_seconds:
                metrics.status = AgentHealthStatus.IDLE
                metrics.is_idle_too_long = True
                idle += 1
            elif metrics.failure_count > 2:
                metrics.status = AgentHealthStatus.DEGRADED
                degraded += 1
            else:
                metrics.status = AgentHealthStatus.HEALTHY
                healthy += 1

        # Calculate health score
        total = len(self.agent_metrics)
        health_score = ((healthy * 100 + degraded * 50 + failed * 0) / (total * 100 * 1.0)) if total > 0 else 0.0

        # Calculate average response time
        avg_response_time = (
            sum(m.response_time_ms for m in self.agent_metrics.values()) /
            len(self.agent_metrics) if self.agent_metrics else 0.0
        )

        # Calculate throughput (tasks per second)
        elapsed = (now - self.last_health_check).total_seconds()
        if elapsed > 0:
            total_completed = sum(m.tasks_completed for m in self.agent_metrics.values())
            throughput = total_completed / elapsed
        else:
            throughput = 0.0

        snapshot = SwarmHealthSnapshot(
            timestamp=now.isoformat(),
            total_agents=total,
            healthy_agents=healthy,
            degraded_agents=degraded,
            failed_agents=failed,
            idle_agents=idle,
            overall_health_score=health_score,
            avg_response_time=avg_response_time,
            task_throughput=throughput
        )

        self.health_history.append(snapshot)
        self.last_health_check = now

        logger.info(
            f"Swarm health check: {healthy} healthy, {degraded} degraded, "
            f"{failed} failed, {idle} idle (score: {health_score:.1f}%)"
        )

        return snapshot

    def get_idle_agents(self) -> List[str]:
        """Get list of idle agents"""
        return [
            agent_id for agent_id, metrics in self.agent_metrics.items()
            if metrics.is_idle_too_long or metrics.status == AgentHealthStatus.IDLE
        ]

    def get_failed_agents(self) -> List[str]:
        """Get list of failed agents"""
        return [
            agent_id for agent_id, metrics in self.agent_metrics.items()
            if metrics.status == AgentHealthStatus.FAILED
        ]

    async def recover_agent(self, agent_id: str) -> bool:
        """Attempt to recover a failed agent"""
        metrics = self.agent_metrics.get(agent_id)
        if not metrics:
            return False

        if metrics.recovery_attempts >= self.recovery_max_attempts:
            logger.warning(f"Agent {agent_id} exceeded max recovery attempts")
            return False

        metrics.recovery_attempts += 1
        metrics.status = AgentHealthStatus.RECOVERING
        metrics.failure_count = 0

        logger.info(f"Attempting recovery for agent {agent_id} (attempt {metrics.recovery_attempts})")
        await asyncio.sleep(1)  # Simulate recovery delay

        metrics.status = AgentHealthStatus.HEALTHY
        logger.info(f"Agent {agent_id} recovered successfully")
        return True

    async def rebalance_load(self) -> Dict[str, int]:
        """Rebalance task load across agents"""
        idle_agents = self.get_idle_agents()
        total_tasks = sum(m.tasks_completed for m in self.agent_metrics.values())
        avg_tasks_per_agent = total_tasks / len(self.agent_metrics) if self.agent_metrics else 0

        rebalanced = 0
        for agent_id in idle_agents:
            logger.info(f"Reassigning idle agent {agent_id}")
            self.agent_metrics[agent_id].status = AgentHealthStatus.HEALTHY
            rebalanced += 1

        return {
            "agents_rebalanced": rebalanced,
            "idle_agents": len(idle_agents),
            "avg_load": avg_tasks_per_agent
        }

    def get_lifecycle_status(self) -> Dict:
        """Get detailed lifecycle status"""
        return {
            "swarm_state": self.swarm_state,
            "total_agents": len(self.agent_metrics),
            "health_checks_completed": len(self.health_history),
            "idle_agents": len(self.get_idle_agents()),
            "failed_agents": len(self.get_failed_agents()),
            "latest_health": self.health_history[-1].__dict__ if self.health_history else None
        }

    def set_swarm_state(self, state: str):
        """Update swarm state"""
        if state in ["initializing", "running", "paused", "error"]:
            self.swarm_state = state
            logger.info(f"Swarm state changed to: {state}")

    def reset_metrics(self):
        """Reset all metrics"""
        for metrics in self.agent_metrics.values():
            metrics.tasks_completed = 0
            metrics.failure_count = 0
            metrics.recovery_attempts = 0
        self.health_history.clear()


if __name__ == "__main__":
    import asyncio

    async def test():
        manager = SwarmLifecycleManager()

        # Register agents
        agent_ids = [f"agent-{i:03d}" for i in range(10)]
        await manager.register_agent_batch(agent_ids)

        # Simulate activity
        for agent_id in agent_ids[:5]:
            manager.update_agent_heartbeat(agent_id, response_time_ms=45.5)
            manager.mark_task_completed(agent_id)

        # Check health
        health = await manager.check_swarm_health()
        print(f"Health snapshot: {health}")

        status = manager.get_lifecycle_status()
        print(f"Status: {status}")

    asyncio.run(test())
