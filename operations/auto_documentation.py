"""
Auto Documentation Engine
Continuously synchronizes documentation with system state
Updates README, architecture docs, and scope files automatically
"""

import logging
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DocumentationChange:
    """Represents a documentation change"""
    timestamp: str
    change_type: str  # "agent_added", "system_updated", "schema_changed"
    affected_files: List[str]
    summary: str


class AutoDocumentationEngine:
    """
    Automatically maintains system documentation
    Syncs: README.md, architecture docs, scope files, changelogs
    """

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.change_history: List[DocumentationChange] = []
        self.last_update = datetime.utcnow()

        # Documentation file paths
        self.readme_path = self.repo_root / "README.md"
        self.architecture_path = self.repo_root / "docs" / "ARCHITECTURE.md"
        self.scope_path = self.repo_root / "repo-tasks" / "SCOPE.md"
        self.changelog_path = self.repo_root / "CHANGELOG.md"

    async def on_agent_created(self, agent_id: str, agent_type: str, domain: str):
        """Handler: agent created"""
        logger.info(f"Documentation: new agent {agent_id} ({agent_type}/{domain})")

        change = DocumentationChange(
            timestamp=datetime.utcnow().isoformat(),
            change_type="agent_added",
            affected_files=["README.md", "ARCHITECTURE.md"],
            summary=f"Added {agent_type} agent {agent_id} in domain {domain}"
        )

        self.change_history.append(change)
        await self._update_agent_documentation(agent_id, agent_type, domain)

    async def on_system_module_added(self, module_name: str, description: str):
        """Handler: new system module added"""
        logger.info(f"Documentation: new module {module_name}")

        change = DocumentationChange(
            timestamp=datetime.utcnow().isoformat(),
            change_type="system_updated",
            affected_files=["ARCHITECTURE.md", "SCOPE.md"],
            summary=f"Added system module {module_name}"
        )

        self.change_history.append(change)
        await self._update_architecture_documentation(module_name, description)

    async def on_schema_updated(self, schema_name: str, schema_definition: Dict):
        """Handler: schema updated"""
        logger.info(f"Documentation: schema updated {schema_name}")

        change = DocumentationChange(
            timestamp=datetime.utcnow().isoformat(),
            change_type="schema_changed",
            affected_files=["ARCHITECTURE.md"],
            summary=f"Updated schema: {schema_name}"
        )

        self.change_history.append(change)
        await self._update_schema_documentation(schema_name, schema_definition)

    async def sync_readme(self, system_stats: Dict) -> bool:
        """Synchronize README.md with current system state"""
        try:
            content = self._generate_readme_content(system_stats)
            self.readme_path.write_text(content)
            logger.info("✓ README.md synchronized")
            return True
        except Exception as e:
            logger.error(f"Failed to sync README: {e}")
            return False

    async def sync_architecture(self, architecture: Dict) -> bool:
        """Synchronize architecture documentation"""
        try:
            content = self._generate_architecture_content(architecture)
            self.architecture_path.parent.mkdir(parents=True, exist_ok=True)
            self.architecture_path.write_text(content)
            logger.info("✓ ARCHITECTURE.md synchronized")
            return True
        except Exception as e:
            logger.error(f"Failed to sync architecture: {e}")
            return False

    async def sync_scope(self, scope: Dict) -> bool:
        """Synchronize scope definition"""
        try:
            content = self._generate_scope_content(scope)
            self.scope_path.parent.mkdir(parents=True, exist_ok=True)
            self.scope_path.write_text(content)
            logger.info("✓ SCOPE.md synchronized")
            return True
        except Exception as e:
            logger.error(f"Failed to sync scope: {e}")
            return False

    async def update_changelog(self, entry: Dict) -> bool:
        """Add entry to changelog"""
        try:
            existing = []
            if self.changelog_path.exists():
                existing = self.changelog_path.read_text().split('\n')

            new_entry = self._format_changelog_entry(entry)
            updated_content = '\n'.join([new_entry] + existing)

            self.changelog_path.write_text(updated_content)
            logger.info("✓ CHANGELOG.md updated")
            return True
        except Exception as e:
            logger.error(f"Failed to update changelog: {e}")
            return False

    async def _update_agent_documentation(self, agent_id: str, agent_type: str, domain: str):
        """Update documentation when agent is added"""
        # Update agent count in README
        # Update agent registry in ARCHITECTURE
        # Add to agent manifest
        pass

    async def _update_architecture_documentation(self, module_name: str, description: str):
        """Update architecture docs when module added"""
        # Add module to architecture overview
        # Update system diagram
        # Update integration section
        pass

    async def _update_schema_documentation(self, schema_name: str, schema_definition: Dict):
        """Update schema documentation"""
        # Add schema to data model section
        # Update relationships
        # Add examples
        pass

    def _generate_readme_content(self, stats: Dict) -> str:
        """Generate README content from system stats"""
        now = datetime.utcnow().isoformat()

        return f"""# Shanee Intelligence - Omniverse Engine

**Status**: {stats.get('status', 'Active')}
**Last Updated**: {now}
**Version**: 0.2.0

## System Overview

Autonomous 500-agent engineering swarm for continuous system evolution.

### Agent Swarm Status
- **Total Agents**: {stats.get('total_agents', 500)}
- **Governors**: {stats.get('governors', 20)}
- **Domain Specialists**: {stats.get('domain_agents', 300)}
- **Workers**: {stats.get('worker_agents', 180)}
- **Health Score**: {stats.get('health_score', 0)}%

### Execution Status
- **Mode**: {stats.get('execution_mode', 'Continuous')}
- **Cycles**: {stats.get('cycle_count', 0)}
- **Tasks Completed**: {stats.get('total_tasks', 0)}
- **Uptime**: {stats.get('uptime', 0)}%

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines.

## License

Proprietary - Shanee Intelligence

---
*This README is automatically synchronized with the live system state.*
"""

    def _generate_architecture_content(self, architecture: Dict) -> str:
        """Generate architecture documentation"""
        return f"""# System Architecture

Last Updated: {datetime.utcnow().isoformat()}

## Overview

{architecture.get('overview', 'See system design')}

## Components

### Core Kernel
- Configuration Management
- Agent Registry
- Task Dispatcher
- Swarm Orchestrator

### HuggingFace Integration
- Inference Client
- Agent Runtime
- Inference Router

### Agent System
- Base Agent
- Governor Agents (20)
- Domain Agents (300)
- Worker Agents (180)

### Operations Layer
- Lifecycle Manager
- Continuous Execution Engine
- Auto Documentation
- Swarm Monitor
- Recovery Engine

## Data Models

See SCOPE.md for detailed specifications.

---
*Automatically maintained by AutoDocumentationEngine*
"""

    def _generate_scope_content(self, scope: Dict) -> str:
        """Generate scope documentation"""
        return f"""# System Scope Definition

Last Updated: {datetime.utcnow().isoformat()}

## Swarm Configuration
- Total Agents: 500
- Governors: 20
- Domain Specialists: 300
- Workers: 180

## Domains
- Unreal Engine
- Backend
- AI Generation
- Multiplayer
- Swift iOS
- Cinematics
- Security
- Networking

## Task Types
- Code Generation
- Debugging
- Testing
- Documentation
- Architecture
- Review
- Deployment
- Research

## Execution Model
- 24/7 continuous operation
- Async/await execution
- HuggingFace inference backend
- GitHub integration

---
*Automatically maintained by AutoDocumentationEngine*
"""

    def _format_changelog_entry(self, entry: Dict) -> str:
        """Format changelog entry"""
        timestamp = entry.get('timestamp', datetime.utcnow().isoformat())
        change_type = entry.get('change_type', 'update')
        description = entry.get('description', 'No description')

        return f"[{timestamp}] {change_type}: {description}"

    def get_documentation_status(self) -> Dict:
        """Get documentation sync status"""
        return {
            "total_changes": len(self.change_history),
            "last_update": self.last_update.isoformat(),
            "files_managed": [
                str(self.readme_path),
                str(self.architecture_path),
                str(self.scope_path),
                str(self.changelog_path)
            ],
            "recent_changes": [
                {
                    "timestamp": c.timestamp,
                    "type": c.change_type,
                    "summary": c.summary
                }
                for c in self.change_history[-5:]
            ]
        }


if __name__ == "__main__":
    import asyncio

    async def test():
        engine = AutoDocumentationEngine()

        # Simulate events
        await engine.on_agent_created("gov-001", "governor", "planning")
        await engine.on_system_module_added("recovery_engine", "Handles agent recovery")

        # Sync documentation
        stats = {
            "status": "Active",
            "total_agents": 500,
            "governors": 20,
            "domain_agents": 300,
            "worker_agents": 180,
            "health_score": 95,
            "cycle_count": 1250,
            "total_tasks": 5000,
            "uptime": 99.8
        }

        await engine.sync_readme(stats)

        # Show status
        status = engine.get_documentation_status()
        print(f"Documentation Status: {status}")

    asyncio.run(test())
