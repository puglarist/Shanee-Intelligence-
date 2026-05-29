#!/usr/bin/env python3
"""
Omniverse Engine 500-Agent Swarm
Main entry point for the autonomous engineering swarm system

Usage:
  python swarm_main.py init     # Initialize swarm
  python swarm_main.py run      # Run swarm (normal mode)
  python swarm_main.py status   # Show status
  python swarm_main.py reset    # Reset swarm state
"""

import asyncio
import json
import sys
import logging
from pathlib import Path
from datetime import datetime

from kernel import (
    SwarmOrchestrator,
    ConfigManager,
    AgentRegistry,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SwarmBootstrap:
    """Bootstrap and manage the swarm system"""

    def __init__(self):
        self.orchestrator = SwarmOrchestrator()
        self.config = self.orchestrator.config
        self.registry = self.orchestrator.registry

    async def initialize(self):
        """Initialize the swarm"""
        logger.info("=" * 70)
        logger.info("OMNIVERSE ENGINE 500-AGENT SWARM INITIALIZATION")
        logger.info("=" * 70)

        try:
            # Step 1: Initialize configuration
            logger.info("\n[1/5] Loading configuration...")
            logger.info(f"  Total agents: {self.config.total_agents}")
            logger.info(f"  Governor agents: {self.config.governor_agents}")
            logger.info(f"  Domain agents: {self.config.domain_agents}")
            logger.info(f"  Worker agents: {self.config.worker_agents}")

            # Step 2: Initialize swarm
            logger.info("\n[2/5] Initializing agent registry...")
            await self.orchestrator.initialize_swarm()

            # Step 3: Verify initialization
            logger.info("\n[3/5] Verifying initialization...")
            health = self.registry.get_swarm_health()
            logger.info(f"  Total agents spawned: {health['total_agents']}")
            logger.info(f"  Idle agents: {health['idle']}")
            logger.info(f"  Success rate: {health['avg_success_rate']:.1%}")

            # Step 4: Initialize memory system
            logger.info("\n[4/5] Initializing memory system...")
            self._initialize_memory()

            # Step 5: Verify system
            logger.info("\n[5/5] System verification...")
            status = self.orchestrator.get_status()
            logger.info(f"  Orchestrator ready: {status['is_running'] or 'standby'}")
            logger.info(f"  Task queue: {status['task_queue_length']} tasks")

            logger.info("\n" + "=" * 70)
            logger.info("✓ SWARM INITIALIZATION COMPLETE")
            logger.info("=" * 70)
            logger.info("\nSwarm is ready for operation.")
            logger.info("Run: python swarm_main.py run")

        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            raise

    async def run(self):
        """Run the swarm"""
        logger.info("=" * 70)
        logger.info("OMNIVERSE ENGINE SWARM - EXECUTION MODE")
        logger.info("=" * 70)
        logger.info(f"Start time: {datetime.utcnow().isoformat()}")
        logger.info(f"Agents: {self.registry.get_total_agent_count()}")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 70 + "\n")

        try:
            # Initialize if needed
            if self.registry.get_total_agent_count() == 0:
                logger.info("First run detected - initializing swarm...")
                await self.initialize()

            # Run execution loop
            await self.orchestrator.start_execution_loop()

        except KeyboardInterrupt:
            logger.info("\n\n" + "=" * 70)
            logger.info("SWARM SHUTDOWN REQUESTED")
            logger.info("=" * 70)
            self.orchestrator.stop()

            # Save state
            logger.info("Saving swarm state...")
            self.registry.save_registry()
            self.orchestrator.config_manager.save_config()

            logger.info("✓ Swarm shutdown complete")

    def show_status(self):
        """Show current swarm status"""
        status = self.orchestrator.get_status()

        print("\n" + "=" * 70)
        print("SWARM STATUS")
        print("=" * 70)
        print(f"Running: {status['is_running']}")
        print(f"Cycle count: {status['cycle_count']}")
        print(f"Current cycle: {status['current_cycle']}")
        print(f"Task queue: {status['task_queue_length']} tasks")
        print(f"Completed tasks: {status['completed_tasks']}")

        health = status['swarm_health']
        print(f"\nSwarm Health:")
        print(f"  Total agents: {health['total_agents']}")
        print(f"  Idle: {health['idle']}")
        print(f"  Busy: {health['busy']}")
        print(f"  Error: {health['error']}")
        print(f"  Total tasks: {health['total_tasks_completed']}")
        print(f"  Success rate: {health['avg_success_rate']:.1%}")

        print("\n" + "=" * 70)

    def reset(self):
        """Reset swarm state"""
        logger.info("Resetting swarm state...")

        # Clear registry
        self.registry.agents.clear()
        self.registry.agents_by_role = {"governor": [], "domain": [], "worker": []}
        self.registry.agents_by_domain = {}

        # Clear task queue
        self.orchestrator.task_queue.clear()
        self.orchestrator.completed_tasks.clear()
        self.orchestrator.cycle_history.clear()
        self.orchestrator.cycle_count = 0

        logger.info("✓ Swarm reset complete")

    def _initialize_memory(self):
        """Initialize memory system"""
        memory_dir = Path("memory")
        memory_dir.mkdir(exist_ok=True)

        # Initialize graph
        (memory_dir / "graph.json").write_text(json.dumps({
            "nodes": [],
            "edges": [],
            "metadata": {"created": datetime.utcnow().isoformat()}
        }, indent=2))

        # Initialize events
        (memory_dir / "events.json").write_text(json.dumps({
            "events": [],
            "metadata": {"created": datetime.utcnow().isoformat()}
        }, indent=2))

        # Initialize decisions
        (memory_dir / "decisions.json").write_text(json.dumps({
            "decisions": [],
            "metadata": {"created": datetime.utcnow().isoformat()}
        }, indent=2))

def main():
    """Main entry point"""
    bootstrap = SwarmBootstrap()

    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    try:
        if command == "init":
            asyncio.run(bootstrap.initialize())
        elif command == "run":
            asyncio.run(bootstrap.run())
        elif command == "status":
            bootstrap.show_status()
        elif command == "reset":
            bootstrap.reset()
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
