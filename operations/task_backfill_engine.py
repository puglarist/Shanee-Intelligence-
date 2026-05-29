"""
Task Backfill Engine
Ensures no idle time in system by continuous R&D task generation
Replenishes queues and expands system automatically
"""

import logging
import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskCategory(Enum):
    """Types of backfill tasks"""
    RESEARCH = "research"              # R&D expansion
    OPTIMIZATION = "optimization"      # Performance improvements
    DEBUGGING = "debugging"            # Bug fixes
    ARCHITECTURE = "architecture"      # System design improvements
    DOCUMENTATION = "documentation"    # Docs updates
    TESTING = "testing"                # Test coverage expansion
    REFACTORING = "refactoring"        # Code quality
    MONITORING = "monitoring"          # System observability


@dataclass
class BackfillTask:
    """Generated backfill task"""
    task_id: str
    category: TaskCategory
    title: str
    description: str
    priority: int
    estimated_time: int
    domain: str
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()


class TaskBackfillEngine:
    """
    Continuously generates tasks to prevent system idle time
    Ensures task queues self-replenish automatically
    """

    def __init__(self):
        self.minimum_backlog = 20
        self.current_backlog_size = 0
        self.generated_tasks: List[BackfillTask] = []
        self.generation_history: List[Dict] = []
        self.is_active = False
        self.task_generation_callback: Optional[Callable] = None

        # Task generation templates
        self.task_templates = self._initialize_templates()

    def _initialize_templates(self) -> Dict[TaskCategory, List[Dict]]:
        """Initialize task generation templates"""
        return {
            TaskCategory.RESEARCH: [
                {
                    "title": "Research LLM fine-tuning approaches",
                    "description": "Investigate optimal fine-tuning strategies for domain-specific models",
                    "domains": ["ai_generation", "backend"]
                },
                {
                    "title": "Benchmark inference performance",
                    "description": "Test HF endpoint performance across different model sizes",
                    "domains": ["ai_generation"]
                }
            ],
            TaskCategory.OPTIMIZATION: [
                {
                    "title": "Optimize agent dispatch logic",
                    "description": "Improve agent selection algorithm for better load balancing",
                    "domains": ["backend"]
                },
                {
                    "title": "Reduce inference latency",
                    "description": "Profile and optimize HF inference pipeline",
                    "domains": ["ai_generation"]
                }
            ],
            TaskCategory.DEBUGGING: [
                {
                    "title": "Debug memory leaks in agent runtime",
                    "description": "Identify and fix memory leaks in long-running agents",
                    "domains": ["backend"]
                },
                {
                    "title": "Fix edge case in task dispatcher",
                    "description": "Address edge cases in task assignment logic",
                    "domains": ["backend"]
                }
            ],
            TaskCategory.ARCHITECTURE: [
                {
                    "title": "Design improved failure recovery",
                    "description": "Architect next generation of recovery mechanisms",
                    "domains": ["backend"]
                },
                {
                    "title": "Plan distributed agent coordination",
                    "description": "Design cross-domain agent coordination protocol",
                    "domains": ["backend", "multiplayer"]
                }
            ],
            TaskCategory.DOCUMENTATION: [
                {
                    "title": "Document agent API",
                    "description": "Create comprehensive agent interface documentation",
                    "domains": ["backend"]
                },
                {
                    "title": "Update architecture guide",
                    "description": "Keep architecture documentation in sync",
                    "domains": ["backend"]
                }
            ],
            TaskCategory.TESTING: [
                {
                    "title": "Add tests for recovery system",
                    "description": "Increase test coverage for auto-recovery",
                    "domains": ["backend"]
                },
                {
                    "title": "Test high-concurrency scenarios",
                    "description": "Test agent swarm under high load",
                    "domains": ["backend"]
                }
            ],
            TaskCategory.REFACTORING: [
                {
                    "title": "Refactor agent lifecycle code",
                    "description": "Improve code quality and maintainability",
                    "domains": ["backend"]
                }
            ],
            TaskCategory.MONITORING: [
                {
                    "title": "Add performance metrics",
                    "description": "Expand observability with new metrics",
                    "domains": ["backend"]
                }
            ]
        }

    def set_task_generation_callback(self, callback: Callable):
        """Set callback to queue generated tasks"""
        self.task_generation_callback = callback
        logger.info("Task generation callback registered")

    def set_minimum_backlog(self, size: int):
        """Set minimum backlog size"""
        self.minimum_backlog = size
        logger.info(f"Minimum backlog set to {size}")

    def update_backlog_size(self, size: int):
        """Update current backlog size"""
        self.current_backlog_size = size

    async def run_backfill_loop(self):
        """
        Run continuous task backfill loop
        Monitors backlog and generates tasks as needed
        """
        self.is_active = True
        logger.info("🔄 Task backfill engine started")

        while self.is_active:
            if self.current_backlog_size < self.minimum_backlog:
                tasks_needed = self.minimum_backlog - self.current_backlog_size
                await self._generate_backfill_tasks(tasks_needed)

            await asyncio.sleep(5)  # Check every 5 seconds

    async def _generate_backfill_tasks(self, count: int):
        """Generate backfill tasks to replenish queue"""
        logger.info(f"Generating {count} backfill tasks...")

        new_tasks = []
        for i in range(count):
            task = self._create_backfill_task(i)
            new_tasks.append(task)
            self.generated_tasks.append(task)

            if self.task_generation_callback:
                try:
                    await self.task_generation_callback(task)
                except Exception as e:
                    logger.error(f"Failed to queue task: {e}")

        # Record generation event
        self.generation_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "tasks_generated": len(new_tasks),
            "backlog_before": self.current_backlog_size,
            "backlog_after": self.current_backlog_size + len(new_tasks)
        })

        logger.info(f"✓ Generated {len(new_tasks)} backfill tasks")

    def _create_backfill_task(self, index: int) -> BackfillTask:
        """Create a backfill task from templates"""
        # Rotate through categories
        categories = list(TaskCategory)
        category = categories[index % len(categories)]

        templates = self.task_templates.get(category, [])
        if not templates:
            template = {
                "title": f"System improvement task {index}",
                "description": f"Auto-generated improvement task",
                "domains": ["backend"]
            }
        else:
            template = templates[index % len(templates)]

        domain = template["domains"][0]
        priority = 5 - (index % 4)  # Priority 1-5

        task = BackfillTask(
            task_id=f"backfill-{datetime.utcnow().timestamp()}-{index}",
            category=category,
            title=template["title"],
            description=template["description"],
            priority=priority,
            estimated_time=300 + (index % 3) * 100,
            domain=domain
        )

        return task

    def get_backfill_status(self) -> Dict:
        """Get backfill engine status"""
        total_generated = len(self.generated_tasks)
        avg_per_hour = (
            (len(self.generation_history) * self.minimum_backlog) /
            (len(self.generation_history) if self.generation_history else 1)
        )

        return {
            "is_active": self.is_active,
            "current_backlog": self.current_backlog_size,
            "minimum_backlog": self.minimum_backlog,
            "backlog_status": "✓ Healthy" if self.current_backlog_size >= self.minimum_backlog else "⚠ Low",
            "total_tasks_generated": total_generated,
            "generation_events": len(self.generation_history),
            "avg_generation_rate": round(avg_per_hour, 1),
            "recent_generations": self.generation_history[-3:] if self.generation_history else []
        }

    def get_generated_tasks(self) -> List[BackfillTask]:
        """Get all generated tasks"""
        return self.generated_tasks.copy()

    def clear_generated_tasks(self):
        """Clear generated task list"""
        self.generated_tasks.clear()

    def stop_backfill(self):
        """Stop backfill loop"""
        logger.info("Task backfill engine stopping...")
        self.is_active = False


if __name__ == "__main__":
    import asyncio

    async def test():
        engine = TaskBackfillEngine()
        engine.set_minimum_backlog(10)
        engine.update_backlog_size(5)

        # Mock callback
        async def on_task_generated(task: BackfillTask):
            pass

        engine.set_task_generation_callback(on_task_generated)

        # Generate some tasks
        await engine._generate_backfill_tasks(5)

        # Show status
        status = engine.get_backfill_status()
        print(f"Backfill Status: {status}")

        # Show generated tasks
        tasks = engine.get_generated_tasks()
        print(f"\nGenerated {len(tasks)} tasks:")
        for task in tasks[:3]:
            print(f"  - {task.title} ({task.category.value})")

    asyncio.run(test())
