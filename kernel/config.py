"""
Swarm Configuration System
Central configuration for the 500-agent Omniverse Engine swarm
"""

from dataclasses import dataclass
from typing import Dict, List
import json
from pathlib import Path

@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    agent_id: str
    role: str  # "governor" | "domain" | "worker"
    domain: str  # e.g., "unreal_engine", "backend", "ai"
    max_concurrency: int = 1
    timeout_seconds: int = 300
    retry_count: int = 3
    hf_model: str = "meta-llama/Llama-2-70b-chat"
    temperature: float = 0.7
    max_tokens: int = 2048

@dataclass
class SwarmConfig:
    """Master configuration for the entire swarm"""
    total_agents: int = 500
    governor_agents: int = 20
    domain_agents: int = 300
    worker_agents: int = 180
    execution_cycle_seconds: int = 300
    max_parallel_agents: int = 50
    max_tasks_per_cycle: int = 100
    validation_required: bool = True
    auto_commit: bool = False  # Start conservative
    log_level: str = "INFO"

    # Hugging Face Configuration
    hf_api_key: str = ""  # From environment
    hf_endpoints: Dict[str, str] = None
    inference_timeout: int = 60

    # GitHub Configuration
    github_token: str = ""  # From environment
    github_repo: str = "puglarist/Shanee-Intelligence-"
    auto_pr: bool = False  # Start conservative
    pr_auto_merge: bool = False

    # Safety limits
    max_task_depth: int = 10
    max_memory_size_mb: int = 500
    max_repo_size_mb: int = 1000

    def __post_init__(self):
        if self.hf_endpoints is None:
            self.hf_endpoints = {
                "default": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat",
                "fast": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B",
                "specialist": "https://api-inference.huggingface.co/models/codellama/CodeLlama-34b"
            }

class ConfigManager:
    """Manages swarm configuration"""

    def __init__(self, config_path: str = "swarm_config.json"):
        self.config_path = Path(config_path)
        self.swarm_config = SwarmConfig()
        self.agent_configs: Dict[str, AgentConfig] = {}
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                data = json.load(f)
                # Load swarm config
                for key, value in data.get("swarm", {}).items():
                    if hasattr(self.swarm_config, key):
                        setattr(self.swarm_config, key, value)

                # Load agent configs
                for agent_id, agent_data in data.get("agents", {}).items():
                    self.agent_configs[agent_id] = AgentConfig(**agent_data)

    def save_config(self):
        """Save configuration to file"""
        data = {
            "swarm": {
                "total_agents": self.swarm_config.total_agents,
                "governor_agents": self.swarm_config.governor_agents,
                "domain_agents": self.swarm_config.domain_agents,
                "worker_agents": self.swarm_config.worker_agents,
                "execution_cycle_seconds": self.swarm_config.execution_cycle_seconds,
                "max_parallel_agents": self.swarm_config.max_parallel_agents,
                "validation_required": self.swarm_config.validation_required,
                "auto_commit": self.swarm_config.auto_commit,
            },
            "agents": {
                agent_id: vars(config)
                for agent_id, config in self.agent_configs.items()
            }
        }

        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_agents_by_role(self, role: str) -> List[AgentConfig]:
        """Get all agents of a specific role"""
        return [config for config in self.agent_configs.values() if config.role == role]

    def get_agents_by_domain(self, domain: str) -> List[AgentConfig]:
        """Get all agents in a specific domain"""
        return [config for config in self.agent_configs.values() if config.domain == domain]

# Global config manager
_config_manager = None

def get_config() -> ConfigManager:
    """Get global config manager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

if __name__ == "__main__":
    config = get_config()
    print(f"Swarm Configuration Loaded")
    print(f"Total Agents: {config.swarm_config.total_agents}")
    print(f"Execution Cycle: {config.swarm_config.execution_cycle_seconds}s")
