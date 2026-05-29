"""
Agent System Module
500-agent swarm with governors, domain specialists, and workers
"""

from .base import BaseAgent, AgentCapabilities
from .governors import GovernorAgent, create_governor_swarm
from .domain import DomainAgent, DOMAIN_EXPERTISE, create_domain_swarm
from .workers import WorkerAgent, create_worker_swarm

__all__ = [
    "BaseAgent",
    "AgentCapabilities",
    "GovernorAgent",
    "create_governor_swarm",
    "DomainAgent",
    "DOMAIN_EXPERTISE",
    "create_domain_swarm",
    "WorkerAgent",
    "create_worker_swarm",
]

__version__ = "0.1.0"
