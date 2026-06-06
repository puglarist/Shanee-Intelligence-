"""Tests for memory system."""

import pytest

from shanee.core.memory import MemorySystem, MemoryType


def test_memory_storage():
    """Test memory storage."""
    system = MemorySystem()

    entry = system.store_memory(
        "agent_1",
        MemoryType.EPISODIC,
        {"action": "task_start", "task_id": "123"}
    )

    assert entry.id is not None
    assert entry.agent_id == "agent_1"
    assert entry.memory_type == MemoryType.EPISODIC


def test_memory_retrieval():
    """Test memory retrieval."""
    system = MemorySystem()

    entry = system.store_memory(
        "agent_1",
        MemoryType.SEMANTIC,
        {"knowledge": "test_knowledge"}
    )

    retrieved = system.retrieve_memory(entry.id)
    assert retrieved is not None
    assert retrieved.content == {"knowledge": "test_knowledge"}


def test_get_agent_memories():
    """Test getting agent memories."""
    system = MemorySystem()

    system.store_memory("agent_1", MemoryType.EPISODIC, {"event": "1"})
    system.store_memory("agent_1", MemoryType.SEMANTIC, {"fact": "2"})
    system.store_memory("agent_1", MemoryType.EPISODIC, {"event": "3"})

    episodic = system.get_agent_memories("agent_1", MemoryType.EPISODIC)
    assert len(episodic) == 2

    all_memories = system.get_agent_memories("agent_1")
    assert len(all_memories) == 3


def test_memory_search():
    """Test memory search."""
    system = MemorySystem()

    system.store_memory("agent_1", MemoryType.SEMANTIC, {"topic": "python"})
    system.store_memory("agent_1", MemoryType.SEMANTIC, {"topic": "javascript"})
    system.store_memory("agent_1", MemoryType.SEMANTIC, {"topic": "python", "level": "advanced"})

    results = system.search_memories("agent_1", "python")
    assert len(results) == 2
