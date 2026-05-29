"""Task coordinator for the Omniverse Engine.

Orchestrates agent execution sequences and manages state updates.
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from orchestrator.agents.earth_sim import (
    TerrainGeneratorAgent,
    BiomeSimulatorAgent,
    CityNodeSystemAgent,
    ClimateStateUpdaterAgent,
)
from orchestrator.tasks import Task, queue


class TaskCoordinator:
    """Coordinates task execution and agent synchronization."""

    def __init__(self):
        """Initialize the task coordinator."""
        self.agents = {
            "terrain": TerrainGeneratorAgent(),
            "biome": BiomeSimulatorAgent(),
            "cities": CityNodeSystemAgent(),
            "climate": ClimateStateUpdaterAgent(),
        }
        self.execution_order = ["terrain", "climate", "biome", "cities"]
        self.world_state_path = Path("memory/world_state.json")

    def execute_cycle(self) -> Dict[str, Any]:
        """Execute a complete swarm simulation cycle.

        Returns:
            Cycle execution results
        """
        cycle_start = time.time()
        results = {
            "cycle_id": datetime.utcnow().isoformat(),
            "agents_executed": [],
            "world_state_updated": False,
            "errors": [],
            "execution_time_ms": 0,
        }

        # Get pending tasks
        pending_tasks = queue.get_pending_tasks()
        if not pending_tasks:
            results["message"] = "No pending tasks"
            return results

        # Execute agents in order
        for agent_name in self.execution_order:
            agent = self.agents.get(agent_name)
            if not agent:
                results["errors"].append(f"Agent {agent_name} not found")
                continue

            # Find matching tasks
            matching_tasks = [
                t for t in pending_tasks
                if agent_name in t.agent_role.lower()
            ]

            if not matching_tasks:
                continue

            # Execute agent with each task
            for task in matching_tasks:
                try:
                    task.mark_running()
                    result = agent.execute(task)

                    # Mark task as completed
                    queue.mark_completed(task.id, result)

                    results["agents_executed"].append({
                        "agent": agent_name,
                        "task_id": task.id,
                        "status": "completed",
                    })
                except Exception as e:
                    results["errors"].append(
                        f"Error executing {agent_name}: {str(e)}"
                    )
                    queue.mark_failed(task.id, str(e))
                    results["agents_executed"].append({
                        "agent": agent_name,
                        "task_id": task.id,
                        "status": "failed",
                        "error": str(e),
                    })

        # Update world state
        if results["agents_executed"]:
            self._update_world_state(results)
            results["world_state_updated"] = True

        cycle_end = time.time()
        results["execution_time_ms"] = int((cycle_end - cycle_start) * 1000)

        return results

    def _update_world_state(self, results: Dict[str, Any]) -> None:
        """Update the world state file with new data.

        Args:
            results: Execution results to incorporate
        """
        try:
            # Load current world state
            world_state = self._load_world_state()

            # Update with new agent results
            completed_tasks = queue.get_completed_tasks()
            for task in completed_tasks:
                if task.result:
                    agent_role = task.agent_role.lower()
                    if "terrain" in agent_role:
                        world_state["state"]["terrain"] = task.result.get("terrain", {})
                    elif "biome" in agent_role:
                        world_state["state"]["biomes"] = task.result.get("biomes", {})
                    elif "climate" in agent_role:
                        world_state["state"]["climate"] = task.result.get("climate_state", {})
                    elif "city" in agent_role:
                        world_state["state"]["cities"] = task.result.get("cities", [])

            # Update metadata
            world_state["timestamp"] = datetime.utcnow().isoformat()
            world_state["version"] = world_state.get("version", 0) + 1

            # Save updated state
            self._save_world_state(world_state)
        except Exception as e:
            print(f"Error updating world state: {e}")

    def _load_world_state(self) -> Dict[str, Any]:
        """Load world state from disk.

        Returns:
            World state dictionary
        """
        if self.world_state_path.exists():
            with open(self.world_state_path, "r") as f:
                return json.load(f)

        return {
            "state": {
                "world": {
                    "version": 1,
                    "timestamp": datetime.utcnow().isoformat(),
                    "initialized": True,
                },
                "terrain": {},
                "climate": {},
                "biomes": {},
                "cities": [],
                "populations": [],
            },
            "timestamp": datetime.utcnow().isoformat(),
            "version": 0,
        }

    def _save_world_state(self, state: Dict[str, Any]) -> None:
        """Save world state to disk.

        Args:
            state: World state to save
        """
        self.world_state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.world_state_path, "w") as f:
            json.dump(state, f, indent=2)

    def get_execution_status(self) -> Dict[str, Any]:
        """Get current execution status.

        Returns:
            Status information
        """
        stats = queue.stats()
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "queue_stats": stats,
            "agents_available": len(self.agents),
            "world_state_path": str(self.world_state_path),
            "world_state_exists": self.world_state_path.exists(),
        }

    def synchronize_agents(self) -> Dict[str, Any]:
        """Synchronize agent status across the system.

        Returns:
            Synchronization results
        """
        agent_states = []

        for agent_name, agent in self.agents.items():
            agent_states.append({
                "name": agent_name,
                "role": agent.role,
                "agent_id": agent.agent_id,
                "status": "active",
            })

        # Save to agents.json
        agents_file = Path("memory/agents.json")
        agents_file.parent.mkdir(parents=True, exist_ok=True)

        with open(agents_file, "w") as f:
            json.dump({
                "agents": agent_states,
                "timestamp": datetime.utcnow().isoformat(),
                "count": len(agent_states),
            }, f, indent=2)

        return {
            "agents_synchronized": len(agent_states),
            "timestamp": datetime.utcnow().isoformat(),
            "agents": agent_states,
        }


# Global coordinator instance
coordinator = TaskCoordinator()
