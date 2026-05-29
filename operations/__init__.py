"""
Operations Layer
24/7 swarm operations, monitoring, recovery, and documentation management
Complete system for autonomous, self-healing, continuously running swarm
"""

from .lifecycle_manager import SwarmLifecycleManager, AgentHealthStatus, AgentHealthMetrics
from .execution_engine import ContinuousExecutionEngine, ExecutionMode, ExecutionMetrics
from .auto_documentation import AutoDocumentationEngine, DocumentationChange
from .swarm_monitor import SwarmMonitor, MonitorMetrics
from .recovery_engine import SwarmRecoveryEngine, FailureEvent, RecoveryStrategy
from .task_backfill_engine import TaskBackfillEngine, BackfillTask, TaskCategory

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
    "SwarmRecoveryEngine",
    "FailureEvent",
    "RecoveryStrategy",
    "TaskBackfillEngine",
    "BackfillTask",
    "TaskCategory",
]

__version__ = "0.2.0"
