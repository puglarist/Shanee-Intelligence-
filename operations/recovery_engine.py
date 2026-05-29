"""
Swarm Recovery Engine
Auto-healing system for detecting and recovering from failures
Restores system consistency without manual intervention
"""

import logging
import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecoveryStrategy(Enum):
    """Recovery strategies"""
    RESTART = "restart"        # Restart failed agent
    REASSIGN = "reassign"      # Reassign to different agent
    ROLLBACK = "rollback"      # Revert to last known good state
    ISOLATE = "isolate"        # Isolate and skip task
    REPLICATE = "replicate"    # Replicate work to backup agent


@dataclass
class FailureEvent:
    """Represents a detected failure"""
    timestamp: str
    agent_id: str
    task_id: str
    error_type: str
    error_message: str
    recovery_strategy: RecoveryStrategy
    recovery_status: str = "pending"  # pending -> in_progress -> recovered -> failed


class SwarmRecoveryEngine:
    """
    Auto-healing system for the swarm
    Detects failures, isolates broken chains, recovers automatically
    """

    def __init__(self):
        self.failure_queue: List[FailureEvent] = []
        self.recovery_history: List[Dict] = []
        self.max_recovery_attempts = 3
        self.recovery_callbacks: Dict[RecoveryStrategy, Callable] = {}
        self.is_active = False

    def register_recovery_callback(self, strategy: RecoveryStrategy, callback: Callable):
        """Register callback for recovery strategy"""
        self.recovery_callbacks[strategy] = callback
        logger.info(f"Registered recovery callback for: {strategy.value}")

    async def on_task_failure(
        self,
        agent_id: str,
        task_id: str,
        error_type: str,
        error_message: str
    ) -> Optional[FailureEvent]:
        """
        Handle task failure
        Determines recovery strategy and initiates recovery
        """
        logger.warning(f"Task failure: {task_id} on agent {agent_id}")

        # Determine recovery strategy
        strategy = self._determine_recovery_strategy(error_type, error_message)

        # Create failure event
        failure = FailureEvent(
            timestamp=datetime.utcnow().isoformat(),
            agent_id=agent_id,
            task_id=task_id,
            error_type=error_type,
            error_message=error_message,
            recovery_strategy=strategy
        )

        self.failure_queue.append(failure)

        # Initiate recovery
        success = await self._execute_recovery(failure)

        if success:
            failure.recovery_status = "recovered"
            logger.info(f"✓ Recovered from failure: {task_id}")
        else:
            failure.recovery_status = "failed"
            logger.error(f"✗ Recovery failed: {task_id}")

        self.recovery_history.append({
            "timestamp": failure.timestamp,
            "task_id": task_id,
            "agent_id": agent_id,
            "strategy": strategy.value,
            "status": failure.recovery_status
        })

        return failure if success else None

    async def on_agent_failure(self, agent_id: str) -> bool:
        """
        Handle agent failure
        Restart or replace agent
        """
        logger.warning(f"Agent failure detected: {agent_id}")

        # Attempt restart
        if await self._restart_agent(agent_id):
            logger.info(f"✓ Agent restarted: {agent_id}")
            return True
        else:
            # Attempt replacement
            if await self._replace_agent(agent_id):
                logger.info(f"✓ Agent replaced: {agent_id}")
                return True

        logger.error(f"✗ Failed to recover agent: {agent_id}")
        return False

    async def on_data_corruption(self, data_location: str) -> bool:
        """
        Handle detected data corruption
        Restore from backup or regenerate
        """
        logger.warning(f"Data corruption detected: {data_location}")

        # Attempt restore from backup
        if await self._restore_from_backup(data_location):
            logger.info(f"✓ Restored from backup: {data_location}")
            return True

        # Attempt regeneration
        if await self._regenerate_data(data_location):
            logger.info(f"✓ Regenerated data: {data_location}")
            return True

        logger.error(f"✗ Failed to repair: {data_location}")
        return False

    def _determine_recovery_strategy(self, error_type: str, error_message: str) -> RecoveryStrategy:
        """
        Determine best recovery strategy based on error
        """
        # Map error types to strategies
        if "timeout" in error_type.lower():
            return RecoveryStrategy.RESTART
        elif "rate_limit" in error_type.lower():
            return RecoveryStrategy.REASSIGN
        elif "validation" in error_type.lower():
            return RecoveryStrategy.ROLLBACK
        elif "permanent" in error_type.lower():
            return RecoveryStrategy.ISOLATE
        else:
            return RecoveryStrategy.REPLICATE

    async def _execute_recovery(self, failure: FailureEvent) -> bool:
        """Execute recovery strategy"""
        strategy = failure.recovery_strategy

        if strategy in self.recovery_callbacks:
            try:
                callback = self.recovery_callbacks[strategy]
                result = await callback(failure)
                return bool(result)
            except Exception as e:
                logger.error(f"Recovery callback error: {e}")
                return False

        # Default implementations
        if strategy == RecoveryStrategy.RESTART:
            return await self._restart_agent(failure.agent_id)
        elif strategy == RecoveryStrategy.REASSIGN:
            return await self._reassign_task(failure.task_id)
        elif strategy == RecoveryStrategy.ROLLBACK:
            return await self._rollback_task(failure.task_id)
        elif strategy == RecoveryStrategy.ISOLATE:
            return await self._isolate_task(failure.task_id)
        else:
            return False

    async def _restart_agent(self, agent_id: str) -> bool:
        """Restart a failed agent"""
        logger.info(f"Restarting agent: {agent_id}")
        await asyncio.sleep(0.5)  # Simulate restart delay
        return True

    async def _replace_agent(self, agent_id: str) -> bool:
        """Replace failed agent with backup"""
        logger.info(f"Replacing agent: {agent_id}")
        await asyncio.sleep(0.5)
        return True

    async def _reassign_task(self, task_id: str) -> bool:
        """Reassign task to different agent"""
        logger.info(f"Reassigning task: {task_id}")
        await asyncio.sleep(0.3)
        return True

    async def _rollback_task(self, task_id: str) -> bool:
        """Rollback task to last known good state"""
        logger.info(f"Rolling back task: {task_id}")
        await asyncio.sleep(0.3)
        return True

    async def _isolate_task(self, task_id: str) -> bool:
        """Isolate failed task and skip"""
        logger.info(f"Isolating task: {task_id}")
        return True

    async def _restore_from_backup(self, location: str) -> bool:
        """Restore data from backup"""
        logger.info(f"Restoring backup: {location}")
        await asyncio.sleep(0.5)
        return True

    async def _regenerate_data(self, location: str) -> bool:
        """Regenerate corrupted data"""
        logger.info(f"Regenerating data: {location}")
        await asyncio.sleep(0.5)
        return True

    async def run_recovery_loop(self):
        """Run continuous recovery monitoring"""
        self.is_active = True
        logger.info("🔧 Recovery engine started")

        while self.is_active:
            # Process failure queue
            while self.failure_queue:
                failure = self.failure_queue.pop(0)
                await self._execute_recovery(failure)

            await asyncio.sleep(1)  # Check every second

    def stop_recovery(self):
        """Stop recovery loop"""
        logger.info("Recovery engine stopping...")
        self.is_active = False

    def get_recovery_status(self) -> Dict:
        """Get recovery engine status"""
        successful = sum(1 for r in self.recovery_history if r.get("status") == "recovered")
        failed = sum(1 for r in self.recovery_history if r.get("status") == "failed")

        return {
            "is_active": self.is_active,
            "pending_failures": len(self.failure_queue),
            "total_recoveries": len(self.recovery_history),
            "successful_recoveries": successful,
            "failed_recoveries": failed,
            "recovery_success_rate": (
                (successful / len(self.recovery_history) * 100)
                if self.recovery_history else 0
            ),
            "recent_recoveries": self.recovery_history[-5:] if self.recovery_history else []
        }

    def clear_history(self):
        """Clear recovery history"""
        self.recovery_history.clear()
        self.failure_queue.clear()
        logger.info("Recovery history cleared")


if __name__ == "__main__":
    import asyncio

    async def test():
        engine = SwarmRecoveryEngine()

        # Register callbacks
        async def on_restart(failure):
            return True

        engine.register_recovery_callback(RecoveryStrategy.RESTART, on_restart)

        # Simulate failures
        await engine.on_task_failure("agent-001", "task-001", "timeout", "Task timed out")
        await engine.on_task_failure("agent-002", "task-002", "validation", "Validation failed")

        # Show status
        status = engine.get_recovery_status()
        print(f"Recovery Status: {status}")

    asyncio.run(test())
