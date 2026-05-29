"""Task queue system for the Omniverse Engine.

Provides in-memory queue with file-based persistence for reliability.
Supports: enqueue, dequeue, mark_complete, retry, and persistence.
"""
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class Task:
    """Represents a task in the queue."""

    id: str
    agent_id: str
    agent_role: str
    task_type: str
    payload: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    retries: int = 0
    max_retries: int = 3
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        """Initialize timestamps if not set."""
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.utcnow().isoformat()

    def mark_running(self) -> None:
        """Mark task as running."""
        self.status = "running"
        self.updated_at = datetime.utcnow().isoformat()

    def mark_completed(self, result: Dict[str, Any]) -> None:
        """Mark task as completed with a result."""
        self.status = "completed"
        self.result = result
        self.updated_at = datetime.utcnow().isoformat()

    def mark_failed(self, error: str) -> None:
        """Mark task as failed."""
        self.status = "failed"
        self.result = {"error": error}
        self.updated_at = datetime.utcnow().isoformat()

    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.retries < self.max_retries

    def retry(self) -> None:
        """Increment retry count and reset status."""
        if self.can_retry():
            self.retries += 1
            self.status = "pending"
            self.updated_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return asdict(self)


class TaskQueue:
    """In-memory task queue with file persistence."""

    def __init__(self, persistence_path: str = "memory/tasks_queue.json"):
        """Initialize the task queue.

        Args:
            persistence_path: Path to persist tasks to disk
        """
        self.persistence_path = Path(persistence_path)
        self.queue: List[Task] = []
        self.completed_tasks: Dict[str, Task] = {}
        self.failed_tasks: Dict[str, Task] = {}

        # Create parent directory if it doesn't exist
        self.persistence_path.parent.mkdir(parents=True, exist_ok=True)

        # Load persisted tasks if they exist
        self._load()

    def enqueue(
        self,
        agent_id: str,
        agent_role: str,
        task_type: str,
        payload: Dict[str, Any],
    ) -> Task:
        """Enqueue a new task.

        Args:
            agent_id: ID of the agent that will execute this task
            agent_role: Role of the agent
            task_type: Type of task
            payload: Task payload/parameters

        Returns:
            The created Task
        """
        task = Task(
            id=str(uuid4()),
            agent_id=agent_id,
            agent_role=agent_role,
            task_type=task_type,
            payload=payload,
        )
        self.queue.append(task)
        self._save()
        return task

    def dequeue(self) -> Optional[Task]:
        """Dequeue the next pending task.

        Returns:
            The next pending task or None if queue is empty
        """
        for task in self.queue:
            if task.status == "pending":
                task.mark_running()
                self._save()
                return task
        return None

    def mark_completed(self, task_id: str, result: Dict[str, Any]) -> bool:
        """Mark a task as completed.

        Args:
            task_id: ID of the task to mark as completed
            result: Result of the task execution

        Returns:
            True if successful, False if task not found
        """
        task = self._find_task(task_id)
        if task:
            task.mark_completed(result)
            self.completed_tasks[task_id] = task
            self._save()
            return True
        return False

    def mark_failed(self, task_id: str, error: str) -> bool:
        """Mark a task as failed.

        Args:
            task_id: ID of the task
            error: Error message

        Returns:
            True if successful, False if task not found
        """
        task = self._find_task(task_id)
        if task:
            if task.can_retry():
                task.retry()
            else:
                task.mark_failed(error)
                self.failed_tasks[task_id] = task
            self._save()
            return True
        return False

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: ID of the task

        Returns:
            The Task or None if not found
        """
        return self._find_task(task_id)

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks.

        Returns:
            List of pending tasks
        """
        return [task for task in self.queue if task.status == "pending"]

    def get_running_tasks(self) -> List[Task]:
        """Get all running tasks.

        Returns:
            List of running tasks
        """
        return [task for task in self.queue if task.status == "running"]

    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks.

        Returns:
            List of completed tasks
        """
        return list(self.completed_tasks.values())

    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks.

        Returns:
            List of failed tasks
        """
        return list(self.failed_tasks.values())

    def stats(self) -> Dict[str, int]:
        """Get queue statistics.

        Returns:
            Dictionary with queue stats
        """
        return {
            "total": len(self.queue) + len(self.completed_tasks) + len(self.failed_tasks),
            "pending": len(self.get_pending_tasks()),
            "running": len(self.get_running_tasks()),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
        }

    def clear(self) -> None:
        """Clear all tasks from the queue."""
        self.queue.clear()
        self.completed_tasks.clear()
        self.failed_tasks.clear()
        self._save()

    def _find_task(self, task_id: str) -> Optional[Task]:
        """Find a task by ID in any collection.

        Args:
            task_id: ID of the task

        Returns:
            The Task or None if not found
        """
        # Check in queue
        for task in self.queue:
            if task.id == task_id:
                return task

        # Check completed
        if task_id in self.completed_tasks:
            return self.completed_tasks[task_id]

        # Check failed
        if task_id in self.failed_tasks:
            return self.failed_tasks[task_id]

        return None

    def _save(self) -> None:
        """Persist tasks to disk."""
        try:
            data = {
                "queue": [task.to_dict() for task in self.queue],
                "completed": {
                    task_id: task.to_dict()
                    for task_id, task in self.completed_tasks.items()
                },
                "failed": {
                    task_id: task.to_dict() for task_id, task in self.failed_tasks.items()
                },
                "saved_at": datetime.utcnow().isoformat(),
            }
            with open(self.persistence_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to persist tasks: {e}")

    def _load(self) -> None:
        """Load tasks from disk if they exist."""
        if not self.persistence_path.exists():
            return

        try:
            with open(self.persistence_path, "r") as f:
                data = json.load(f)

            # Load queue
            for task_data in data.get("queue", []):
                task = Task(**task_data)
                self.queue.append(task)

            # Load completed
            for task_id, task_data in data.get("completed", {}).items():
                task = Task(**task_data)
                self.completed_tasks[task_id] = task

            # Load failed
            for task_id, task_data in data.get("failed", {}).items():
                task = Task(**task_data)
                self.failed_tasks[task_id] = task
        except Exception as e:
            print(f"Warning: Failed to load persisted tasks: {e}")


# Global queue instance
queue = TaskQueue()
