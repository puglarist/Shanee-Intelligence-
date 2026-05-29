"""
Swarm Kernel
Core orchestration system for the 500-agent Omniverse Engine
"""

from .config import ConfigManager, get_config
from .registry import AgentRegistry, AgentStatus
from .orchestrator import SwarmOrchestrator, ExecutionCycle
from .dispatcher import TaskDispatcher, Task, TaskType, TaskPriority

__all__ = [
    "ConfigManager",
    "get_config",
    "AgentRegistry",
    "AgentStatus",
    "SwarmOrchestrator",
    "ExecutionCycle",
    "TaskDispatcher",
    "Task",
    "TaskType",
    "TaskPriority"
]

__version__ = "0.1.0"
