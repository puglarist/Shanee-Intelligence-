"""Tests for agent functionality."""

import pytest

from shanee.core.agents import Agent, AgentConfig, AgentManager, AgentStatus


def test_agent_creation():
    """Test agent creation."""
    config = AgentConfig(name="test_agent", description="Test agent")
    agent = Agent(config=config)

    assert agent.config.name == "test_agent"
    assert agent.status == AgentStatus.IDLE
    assert agent.id is not None


def test_agent_status_update():
    """Test agent status updates."""
    config = AgentConfig(name="test_agent")
    agent = Agent(config=config)

    agent.update_status(AgentStatus.RUNNING)
    assert agent.status == AgentStatus.RUNNING

    agent.update_status(AgentStatus.COMPLETED)
    assert agent.status == AgentStatus.COMPLETED


def test_agent_context():
    """Test agent context management."""
    config = AgentConfig(name="test_agent")
    agent = Agent(config=config)

    agent.set_context("key1", "value1")
    assert agent.get_context("key1") == "value1"

    agent.set_context("key2", {"nested": "data"})
    assert agent.get_context("key2") == {"nested": "data"}


def test_agent_history():
    """Test agent execution history."""
    config = AgentConfig(name="test_agent")
    agent = Agent(config=config)

    agent.add_to_history({"event": "started"})
    agent.add_to_history({"event": "task_completed"})

    assert len(agent.execution_history) == 2
    assert agent.execution_history[0]["event"] == "started"


def test_agent_manager_creation():
    """Test agent manager creation."""
    manager = AgentManager()
    config = AgentConfig(name="test_agent")

    agent = manager.create_agent(config)

    assert agent.id is not None
    assert manager.get_agent(agent.id) == agent


def test_agent_manager_listing():
    """Test agent manager listing."""
    manager = AgentManager()

    config1 = AgentConfig(name="agent1")
    config2 = AgentConfig(name="agent2")

    agent1 = manager.create_agent(config1)
    agent2 = manager.create_agent(config2)

    agents = manager.list_agents()
    assert len(agents) == 2


def test_agent_groups():
    """Test agent group management."""
    manager = AgentManager()

    config1 = AgentConfig(name="agent1")
    config2 = AgentConfig(name="agent2")

    agent1 = manager.create_agent(config1)
    agent2 = manager.create_agent(config2)

    assert manager.create_group("team_a", [agent1.id, agent2.id])

    group_agents = manager.get_group_agents("team_a")
    assert len(group_agents) == 2
