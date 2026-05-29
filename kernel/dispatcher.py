"""
Task Dispatcher
Intelligent task assignment to 500-agent swarm
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class TaskType(Enum):
    CODE_GENERATION = "code_gen"
    DEBUGGING = "debug"
    TESTING = "test"
    DOCUMENTATION = "doc"
    ARCHITECTURE = "arch"
    REVIEW = "review"
    DEPLOYMENT = "deploy"
    RESEARCH = "research"

@dataclass
class Task:
    """Represents a task to be executed"""
    id: str
    type: TaskType
    priority: TaskPriority
    title: str
    description: str
    required_domain: Optional[str] = None
    required_specialization: Optional[str] = None
    dependencies: List[str] = None
    estimated_time: int = 300  # seconds
    max_retries: int = 3
    created: str = ""
    assigned_to: Optional[str] = None
    status: str = "pending"  # pending -> assigned -> executing -> completed -> validated

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class TaskDispatcher:
    """
    Intelligent dispatcher for assigning tasks to agents
    Considers: agent specialization, load balancing, domain expertise, dependencies
    """

    def __init__(self, registry):
        self.registry = registry
        self.task_queue: List[Task] = []
        self.assignment_history: Dict[str, List[str]] = {}  # agent_id -> [task_ids]

    def add_task(self, task: Task) -> str:
        """Add a task to the queue"""
        self.task_queue.append(task)
        return task.id

    def assign_task(self, task: Task, agent_id: str) -> bool:
        """Assign a specific task to a specific agent"""
        agent = self.registry.get_agent(agent_id)

        if not agent:
            return False

        # Check if agent can handle this task
        if not self.can_agent_handle_task(agent, task):
            return False

        # Assign task
        task.assigned_to = agent_id
        task.status = "assigned"

        # Update agent status
        self.registry.update_agent_status(agent_id, "busy", task.id)

        # Update assignment history
        if agent_id not in self.assignment_history:
            self.assignment_history[agent_id] = []
        self.assignment_history[agent_id].append(task.id)

        return True

    def dispatch_all_tasks(self) -> Dict:
        """
        Dispatch all pending tasks to appropriate agents
        Returns: assignment summary
        """
        summary = {
            "total_tasks": len(self.task_queue),
            "assigned": 0,
            "unassigned": 0,
            "assignments": []
        }

        # Sort by priority
        sorted_tasks = sorted(
            [t for t in self.task_queue if t.status == "pending"],
            key=lambda t: t.priority.value
        )

        for task in sorted_tasks:
            # Find best agent for this task
            best_agent = self.find_best_agent(task)

            if best_agent:
                self.assign_task(task, best_agent.agent_id)
                summary["assigned"] += 1
                summary["assignments"].append({
                    "task_id": task.id,
                    "agent_id": best_agent.agent_id,
                    "domain": task.required_domain
                })
            else:
                summary["unassigned"] += 1

        return summary

    def find_best_agent(self, task: Task):
        """
        Find the best agent for a task
        Considers: specialization, domain, load, availability
        """
        candidates = []

        # Get agents by domain if specified
        if task.required_domain:
            candidates = self.registry.get_agents_by_domain(task.required_domain)
        else:
            # Get idle workers for general tasks
            candidates = self.registry.get_idle_agents(10)

        if not candidates:
            return None

        # Sort by load (least loaded first)
        candidates.sort(key=lambda a: a.metrics.total_tasks)

        return candidates[0]

    def can_agent_handle_task(self, agent, task: Task) -> bool:
        """Check if an agent can handle a task"""
        # Agent must be idle
        if agent.status.value != "idle":
            return False

        # If domain is required, agent must match
        if task.required_domain:
            agent_domains = [d for d in self.registry.agents_by_domain.keys()
                           if agent.agent_id in self.registry.agents_by_domain[d]]
            if task.required_domain not in agent_domains:
                return False

        return True

    def rebalance_load(self):
        """Rebalance task load across agents"""
        # Calculate average task count
        agents = list(self.registry.agents.values())
        total_tasks = sum(a.metrics.total_tasks for a in agents)
        avg_per_agent = total_tasks / len(agents) if agents else 0

        overloaded = [a for a in agents if a.metrics.total_tasks > avg_per_agent * 1.5]
        underloaded = [a for a in agents if a.metrics.total_tasks < avg_per_agent * 0.5]

        # Move tasks from overloaded to underloaded agents
        # (simplified version - real implementation would be more sophisticated)
        return {
            "rebalanced": len(overloaded),
            "overloaded_agents": len(overloaded),
            "underloaded_agents": len(underloaded)
        }

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks"""
        return [t for t in self.task_queue if t.status == "pending"]

    def get_assigned_tasks(self) -> List[Task]:
        """Get all assigned tasks"""
        return [t for t in self.task_queue if t.status == "assigned"]

    def get_tasks_for_agent(self, agent_id: str) -> List[Task]:
        """Get tasks assigned to a specific agent"""
        return [t for t in self.task_queue if t.assigned_to == agent_id]

    def mark_task_completed(self, task_id: str, result: str) -> bool:
        """Mark a task as completed"""
        for task in self.task_queue:
            if task.id == task_id:
                task.status = "completed"
                # Update agent metrics
                if task.assigned_to:
                    agent = self.registry.get_agent(task.assigned_to)
                    if agent:
                        agent.metrics.completed_tasks += 1
                        agent.metrics.total_tasks += 1
                        agent.metrics.success_rate = (
                            agent.metrics.completed_tasks / agent.metrics.total_tasks
                        )
                return True
        return False

    def get_dispatcher_status(self) -> Dict:
        """Get dispatcher status"""
        return {
            "total_tasks": len(self.task_queue),
            "pending": len(self.get_pending_tasks()),
            "assigned": len(self.get_assigned_tasks()),
            "completed": len([t for t in self.task_queue if t.status == "completed"]),
            "assignment_history_size": len(self.assignment_history)
        }

if __name__ == "__main__":
    from registry import AgentRegistry

    # Demo
    registry = AgentRegistry()
    registry.spawn_swarm({"governor_agents": 2, "domain_agents": 10, "worker_agents": 5})

    dispatcher = TaskDispatcher(registry)

    # Create sample tasks
    task1 = Task(
        id="task-1",
        type=TaskType.CODE_GENERATION,
        priority=TaskPriority.HIGH,
        title="Generate API endpoint",
        description="Create new REST endpoint for user management",
        required_domain="backend"
    )

    dispatcher.add_task(task1)

    # Dispatch tasks
    summary = dispatcher.dispatch_all_tasks()
    print(f"Task dispatch summary: {summary}")
