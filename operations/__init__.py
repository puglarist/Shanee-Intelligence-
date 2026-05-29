"""
Operations Layer
24/7 swarm operations, monitoring, recovery, and documentation management
"""

from .lifecycle_manager import SwarmLifecycleManager, AgentHealthStatus, AgentHealthMetrics
from .execution_engine import ContinuousExecutionEngine, ExecutionMode, ExecutionMetrics
from .auto_documentation import AutoDocumentationEngine, DocumentationChange
from .swarm_monitor import SwarmMonitor, MonitorMetrics

__all__ = [
    "SwarmLifecycleManager",
    "AgentHealthStatus",
    "AgentHealthMetrics",
    "ContinuousExecutionEngine",
    "ExecutionMode",
    "ExecutionMetrics",
    "AutoDocumentationEngine",
    "DocumentationChange",
    "SwarmMonitor",
    "MonitorMetrics",
]

__version__ = "0.1.0"
