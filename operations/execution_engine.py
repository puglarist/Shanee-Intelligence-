"""
Continuous Execution Engine
Ensures perpetual 24/7 task execution without stalls
Maintains minimum task backlog and prevents idle time
"""

import logging
import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """Execution modes"""
    CONTINUOUS = "continuous"  # 24/7 operation
    SCHEDULED = "scheduled"     # Scheduled windows
    BURST = "burst"             # High-intensity bursts
    IDLE = "idle"               # No active execution


@dataclass
class ExecutionMetrics:
    """Execution performance metrics"""
    cycle_count: int = 0
    total_tasks_executed: int = 0
    total_tasks_failed: int = 0
    avg_cycle_time: float = 0.0
    min_cycle_time: float = float('inf')
    max_cycle_time: float = 0.0
    execution_uptime: float = 0.0  # percentage
    idle_time: float = 0.0  # percentage


class ContinuousExecutionEngine:
    """
    Ensures 24/7 continuous task execution
    Prevents idle time by maintaining task backlog
    Manages execution cycles and throughput
    """

    def __init__(self):
        self.execution_mode = ExecutionMode.CONTINUOUS
        self.is_active = False
        self.minimum_backlog_size = 10
        self.task_generation_callback: Optional[Callable] = None
        self.task_execution_callback: Optional[Callable] = None
        self.current_backlog_size = 0
        self.metrics = ExecutionMetrics()
        self.execution_history: List[Dict] = []
        self.cycle_times: List[float] = []
        self.start_time = None

    def set_task_generation_callback(self, callback: Callable):
        """Set callback for task generation"""
        self.task_generation_callback = callback
        logger.info("Task generation callback registered")

    def set_task_execution_callback(self, callback: Callable):
        """Set callback for task execution"""
        self.task_execution_callback = callback
        logger.info("Task execution callback registered")

    def set_minimum_backlog(self, size: int):
        """Set minimum backlog size threshold"""
        self.minimum_backlog_size = size
        logger.info(f"Minimum backlog set to {size}")

    async def run_execution_loop(self):
        """
        Main 24/7 execution loop
        WHILE system_active:
          CHECK backlog
          IF backlog < threshold:
            GENERATE new tasks
          EXECUTE available tasks
          VALIDATE outputs
        """
        self.is_active = True
        self.start_time = datetime.utcnow()
        logger.info("🚀 Starting continuous execution loop (24/7 mode)")

        try:
            while self.is_active:
                await self._execute_cycle()
        except KeyboardInterrupt:
            logger.info("Execution loop interrupted")
        except Exception as e:
            logger.error(f"Execution loop error: {e}")
        finally:
            await self._shutdown()

    async def _execute_cycle(self):
        """Execute one cycle of the engine"""
        cycle_start = datetime.utcnow()
        self.metrics.cycle_count += 1

        try:
            # Phase 1: Check backlog
            await self._check_and_replenish_backlog()

            # Phase 2: Execute tasks
            tasks_executed = await self._execute_available_tasks()
            self.metrics.total_tasks_executed += tasks_executed

            # Phase 3: Record metrics
            cycle_time = (datetime.utcnow() - cycle_start).total_seconds()
            self.cycle_times.append(cycle_time)
            self._update_metrics(cycle_time, tasks_executed)

            # Ensure minimum cycle time (no spinning)
            min_cycle_sleep = 0.1  # 100ms minimum
            if cycle_time < min_cycle_sleep:
                await asyncio.sleep(min_cycle_sleep - cycle_time)

        except Exception as e:
            logger.error(f"Cycle execution error: {e}")
            self.metrics.total_tasks_failed += 1

    async def _check_and_replenish_backlog(self):
        """
        Check task backlog and replenish if needed
        Ensures continuous execution without idle time
        """
        if self.current_backlog_size < self.minimum_backlog_size:
            tasks_needed = self.minimum_backlog_size - self.current_backlog_size

            if self.task_generation_callback:
                try:
                    new_tasks = await self.task_generation_callback(tasks_needed)
                    self.current_backlog_size += len(new_tasks)
                    logger.info(f"Backlog replenished: +{len(new_tasks)} tasks (total: {self.current_backlog_size})")
                except Exception as e:
                    logger.error(f"Task generation failed: {e}")

    async def _execute_available_tasks(self) -> int:
        """Execute tasks from backlog"""
        if not self.task_execution_callback or self.current_backlog_size == 0:
            return 0

        try:
            tasks_executed = await self.task_execution_callback()
            if tasks_executed > 0:
                self.current_backlog_size = max(0, self.current_backlog_size - tasks_executed)
            return tasks_executed
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return 0

    def _update_metrics(self, cycle_time: float, tasks_executed: int):
        """Update execution metrics"""
        # Update cycle time statistics
        if cycle_time < self.metrics.min_cycle_time:
            self.metrics.min_cycle_time = cycle_time
        if cycle_time > self.metrics.max_cycle_time:
            self.metrics.max_cycle_time = cycle_time

        # Update average cycle time (exponential moving average)
        if self.metrics.cycle_count == 1:
            self.metrics.avg_cycle_time = cycle_time
        else:
            self.metrics.avg_cycle_time = (
                (self.metrics.avg_cycle_time * 0.8) +
                (cycle_time * 0.2)
            )

        # Record execution history
        self.execution_history.append({
            "cycle": self.metrics.cycle_count,
            "timestamp": datetime.utcnow().isoformat(),
            "tasks_executed": tasks_executed,
            "cycle_time": round(cycle_time, 3),
            "backlog_size": self.current_backlog_size
        })

    def update_backlog(self, count: int):
        """Update current backlog size"""
        self.current_backlog_size = max(0, count)

    def add_to_backlog(self, count: int):
        """Add tasks to backlog"""
        self.current_backlog_size += count

    def remove_from_backlog(self, count: int):
        """Remove tasks from backlog"""
        self.current_backlog_size = max(0, self.current_backlog_size - count)

    def set_execution_mode(self, mode: ExecutionMode):
        """Set execution mode"""
        self.execution_mode = mode
        logger.info(f"Execution mode set to: {mode.value}")

    def stop_execution(self):
        """Stop execution loop"""
        logger.info("Stopping execution engine...")
        self.is_active = False

    async def _shutdown(self):
        """Clean up on shutdown"""
        if self.start_time:
            uptime = (datetime.utcnow() - self.start_time).total_seconds()
            self.metrics.execution_uptime = uptime

        logger.info(f"Execution engine shutdown complete")
        logger.info(f"  Total cycles: {self.metrics.cycle_count}")
        logger.info(f"  Tasks executed: {self.metrics.total_tasks_executed}")
        logger.info(f"  Avg cycle time: {self.metrics.avg_cycle_time:.3f}s")

    def get_execution_status(self) -> Dict:
        """Get execution engine status"""
        return {
            "is_active": self.is_active,
            "mode": self.execution_mode.value,
            "cycle_count": self.metrics.cycle_count,
            "total_tasks_executed": self.metrics.total_tasks_executed,
            "total_tasks_failed": self.metrics.total_tasks_failed,
            "current_backlog": self.current_backlog_size,
            "minimum_backlog": self.minimum_backlog_size,
            "avg_cycle_time": round(self.metrics.avg_cycle_time, 3),
            "recent_cycles": self.execution_history[-5:] if self.execution_history else []
        }

    def get_metrics(self) -> ExecutionMetrics:
        """Get current metrics"""
        return self.metrics

    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = ExecutionMetrics()
        self.execution_history.clear()
        self.cycle_times.clear()


if __name__ == "__main__":
    import asyncio

    async def test():
        engine = ContinuousExecutionEngine()

        # Mock callbacks
        async def generate_tasks(count: int):
            return list(range(count))

        async def execute_tasks():
            await asyncio.sleep(0.05)
            return 3

        engine.set_task_generation_callback(generate_tasks)
        engine.set_task_execution_callback(execute_tasks)
        engine.set_minimum_backlog(5)
        engine.update_backlog(5)

        # Run for a few cycles
        async def run_limited():
            for _ in range(3):
                await engine._execute_cycle()
            engine.stop_execution()

        await run_limited()

        # Show status
        status = engine.get_execution_status()
        print(f"Execution Status: {status}")

    asyncio.run(test())
