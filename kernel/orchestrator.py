"""
Swarm Orchestrator
Central controller for the 500-agent autonomous swarm
Manages: execution cycles, task dispatch, coordination using HF-powered agents
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import json
import logging

from config import ConfigManager, SwarmConfig
from registry import AgentRegistry, AgentStatus
from huggingface import HFClient, InferenceRouter, AgentRuntime
from agents import (
    create_governor_swarm,
    create_domain_swarm,
    create_worker_swarm
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExecutionCycle:
    """Represents one execution cycle of the swarm"""

    def __init__(self, cycle_id: str):
        self.cycle_id = cycle_id
        self.timestamp = datetime.utcnow().isoformat()
        self.status = "initializing"  # initializing -> reading -> planning -> executing -> validating -> complete
        self.agents_active = 0
        self.tasks_generated = 0
        self.tasks_assigned = 0
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.duration_seconds = 0.0

class SwarmOrchestrator:
    """
    Central orchestrator for the 500-agent Omniverse Engine swarm
    Integrates HuggingFace inference and intelligent agent routing
    """

    def __init__(self, config_path: str = "swarm_config.json"):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.swarm_config
        self.registry = AgentRegistry(self.config_manager)

        # HuggingFace integration
        self.hf_client = HFClient(
            api_key=self.config.hf_api_key,
            endpoints=self.config.hf_endpoints
        )
        self.inference_router = InferenceRouter(self.hf_client)
        self.agent_runtime = AgentRuntime(self.hf_client)

        # Agent swarm (created on demand)
        self.governors = []
        self.domain_agents = []
        self.worker_agents = []
        self.all_agents = {}

        # Execution state
        self.is_running = False
        self.current_cycle: Optional[ExecutionCycle] = None
        self.cycle_history: List[ExecutionCycle] = []
        self.cycle_count = 0

        # Task state
        self.task_queue: List[Dict] = []
        self.completed_tasks: List[Dict] = []

        logger.info(f"SwarmOrchestrator initialized with {self.config.total_agents} agents")
        logger.info(f"HF Integration: router ready with {len(self.inference_router.routes)} route strategies")

    async def initialize_swarm(self):
        """Initialize the swarm with HF-powered agents"""
        logger.info("Initializing 500-agent HF-powered swarm...")

        # Create agent swarms
        logger.info("Creating governor agents...")
        self.governors = await create_governor_swarm(
            count=self.config.governor_agents,
            router=self.inference_router
        )

        logger.info("Creating domain specialist agents...")
        self.domain_agents = await create_domain_swarm(
            count=self.config.domain_agents,
            router=self.inference_router
        )

        logger.info("Creating worker agents...")
        self.worker_agents = await create_worker_swarm(
            count=self.config.worker_agents,
            router=self.inference_router
        )

        # Register all agents in runtime
        all_agents = self.governors + self.domain_agents + self.worker_agents
        for agent in all_agents:
            self.agent_runtime.register_agent(agent.context)
            self.all_agents[agent.agent_id] = agent

        # Also register in legacy registry for compatibility
        spawned = self.registry.spawn_swarm(self.config)
        logger.info(f"✓ Spawned {len(spawned['governor'])} governor agents")
        logger.info(f"✓ Spawned {len(spawned['domain'])} domain agents")
        logger.info(f"✓ Spawned {len(spawned['worker'])} worker agents")

        # Save configuration and registry
        self.config_manager.save_config()
        self.registry.save_registry()

        logger.info(f"✓ HF-Powered swarm ready with {len(all_agents)} active agents")
        logger.info(f"✓ Inference router configured with {len(self.inference_router.routes)} strategies")

    async def start_execution_loop(self):
        """Start the main autonomous execution loop"""
        logger.info("🚀 Starting execution loop...")
        self.is_running = True

        try:
            while self.is_running:
                await self.execute_cycle()
                await asyncio.sleep(self.config.execution_cycle_seconds)
        except KeyboardInterrupt:
            logger.info("Execution loop interrupted by user")
        except Exception as e:
            logger.error(f"Execution loop error: {e}")
            self.is_running = False

    async def execute_cycle(self):
        """Execute one cycle of the swarm"""
        self.cycle_count += 1
        cycle = ExecutionCycle(f"cycle-{self.cycle_count}")
        self.current_cycle = cycle

        logger.info(f"\n{'='*60}")
        logger.info(f"EXECUTION CYCLE {self.cycle_count}")
        logger.info(f"{'='*60}")

        start_time = datetime.utcnow()

        try:
            # Stage 1: Read repo state
            logger.info("📖 STAGE 1: Reading repo state...")
            await self.read_repo_state()
            cycle.status = "reading"

            # Stage 2: Generate tasks
            logger.info("🧠 STAGE 2: Generating tasks (Governor agents)...")
            await self.generate_tasks()
            cycle.status = "planning"
            logger.info(f"Generated {len(self.task_queue)} tasks")

            # Stage 3: Assign tasks
            logger.info("📋 STAGE 3: Assigning tasks to swarm...")
            await self.assign_tasks()
            cycle.status = "assigning"

            # Stage 4: Execute tasks
            logger.info("⚙️  STAGE 4: Executing tasks (Domain + Worker agents)...")
            await self.execute_tasks()
            cycle.status = "executing"

            # Stage 5: Validate outputs
            logger.info("✅ STAGE 5: Validating outputs...")
            await self.validate_outputs()
            cycle.status = "validating"

            # Stage 6: Update repo
            logger.info("💾 STAGE 6: Updating repository...")
            await self.update_repository()

            cycle.status = "complete"

        except Exception as e:
            logger.error(f"Cycle error: {e}")
            cycle.status = "error"

        finally:
            # Record cycle
            end_time = datetime.utcnow()
            cycle.duration_seconds = (end_time - start_time).total_seconds()
            self.cycle_history.append(cycle)

            # Log summary
            health = self.registry.get_swarm_health()
            logger.info(f"\n✓ Cycle {self.cycle_count} complete")
            logger.info(f"  Duration: {cycle.duration_seconds:.2f}s")
            logger.info(f"  Swarm status: {health['idle']} idle, {health['busy']} busy, {health['error']} errors")
            logger.info(f"  Total tasks completed this session: {health['total_tasks_completed']}")

    async def read_repo_state(self):
        """Read current repository state"""
        # TODO: Implement actual repo reading
        # For now, placeholder
        logger.info("  Reading: repo structure, tasks, memory")

    async def generate_tasks(self):
        """Generate tasks using Governor agents with HF inference"""
        # Use 5 governors per cycle for task generation
        governors_to_use = self.governors[:min(5, len(self.governors))]

        for governor in governors_to_use:
            try:
                # Create a task for the governor to reason about
                task = {
                    "id": f"task-{self.cycle_count}-{governor.agent_id}",
                    "generated_by": governor.agent_id,
                    "priority": "medium",
                    "status": "pending",
                    "created": datetime.utcnow().isoformat()
                }
                self.task_queue.append(task)

                # Update agent status
                self.registry.update_agent_status(governor.agent_id, AgentStatus.BUSY, task["id"])
                logger.info(f"Governor {governor.agent_id} generating tasks via HF inference...")

            except Exception as e:
                logger.error(f"Task generation by {governor.agent_id} failed: {e}")

    async def assign_tasks(self):
        """Assign tasks to domain and worker agents"""
        for task in self.task_queue:
            # Find appropriate agent based on task type
            idle_agents = self.registry.get_idle_agents(1)

            if idle_agents:
                agent = idle_agents[0]
                task["assigned_to"] = agent.agent_id
                task["status"] = "assigned"
                self.registry.update_agent_status(agent.agent_id, AgentStatus.BUSY, task["id"])

    async def execute_tasks(self):
        """Execute assigned tasks"""
        for task in self.task_queue:
            if task["status"] == "assigned":
                # In reality: Call HF model to execute task
                # For now: Mark as completed
                task["status"] = "completed"
                task["result"] = "placeholder_output"

                if task["assigned_to"]:
                    self.registry.update_agent_status(task["assigned_to"], AgentStatus.IDLE)

    async def validate_outputs(self):
        """Validate task outputs before merge"""
        for task in self.task_queue:
            if task["status"] == "completed":
                # TODO: Implement validation logic
                # Check: syntax, tests, schema, etc.
                task["validated"] = True
                self.completed_tasks.append(task)

    async def update_repository(self):
        """Update repository with validated outputs"""
        # TODO: Implement repo update
        # - Create commits
        # - Create PRs
        # - Trigger CI
        pass

    def stop(self):
        """Stop the execution loop"""
        logger.info("Stopping execution loop...")
        self.is_running = False

    def get_status(self) -> Dict:
        """Get current orchestrator status"""
        swarm_health = self.registry.get_swarm_health()

        return {
            "is_running": self.is_running,
            "cycle_count": self.cycle_count,
            "current_cycle": self.current_cycle.cycle_id if self.current_cycle else None,
            "task_queue_length": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "swarm_health": swarm_health,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def run(self):
        """Run the orchestrator"""
        try:
            # Initialize if first run
            if self.registry.get_total_agent_count() == 0:
                await self.initialize_swarm()

            # Start execution loop
            await self.start_execution_loop()
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            raise

if __name__ == "__main__":
    import sys

    orchestrator = SwarmOrchestrator()

    # Simple CLI
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            print("Initializing swarm...")
            asyncio.run(orchestrator.initialize_swarm())
        elif sys.argv[1] == "run":
            print("Running orchestrator...")
            asyncio.run(orchestrator.run())
        elif sys.argv[1] == "status":
            print(json.dumps(orchestrator.get_status(), indent=2))
    else:
        print("Usage: python orchestrator.py [init|run|status]")
