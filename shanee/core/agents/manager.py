"""Agent lifecycle and coordination management."""

from typing import Dict, List, Optional

from .agent import Agent, AgentConfig, AgentStatus


class AgentManager:
    """Manages agent lifecycle and coordination."""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.agent_groups: Dict[str, List[str]] = {}

    def create_agent(self, config: AgentConfig) -> Agent:
        """Create and register a new agent."""
        agent = Agent(config=config)
        self.agents[agent.id] = agent
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    def list_agents(self, status: Optional[AgentStatus] = None) -> List[Agent]:
        """List all agents, optionally filtered by status."""
        agents = list(self.agents.values())
        if status:
            agents = [a for a in agents if a.status == status]
        return agents

    def terminate_agent(self, agent_id: str) -> bool:
        """Terminate an agent."""
        agent = self.agents.get(agent_id)
        if agent:
            agent.update_status(AgentStatus.TERMINATED)
            return True
        return False

    def create_group(self, group_name: str, agent_ids: List[str]) -> bool:
        """Create an agent group for coordination."""
        if group_name in self.agent_groups:
            return False
        self.agent_groups[group_name] = agent_ids
        return True

    def get_group_agents(self, group_name: str) -> Optional[List[Agent]]:
        """Get all agents in a group."""
        agent_ids = self.agent_groups.get(group_name)
        if not agent_ids:
            return None
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]

    def broadcast_to_group(self, group_name: str, message: dict) -> List[str]:
        """Broadcast message to all agents in a group."""
        agents = self.get_group_agents(group_name)
        if not agents:
            return []

        sent_to = []
        for agent in agents:
            if agent.status != AgentStatus.TERMINATED:
                agent.add_to_history({
                    "event": "message_received",
                    "message": message
                })
                sent_to.append(agent.id)
        return sent_to
