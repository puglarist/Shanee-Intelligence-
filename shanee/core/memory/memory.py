"""Memory system for agents."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Types of memory."""
    EPISODIC = "episodic"      # Task execution history
    SEMANTIC = "semantic"       # Knowledge base
    WORKING = "working"         # Current context


class MemoryEntry(BaseModel):
    """Single memory entry."""
    id: str
    agent_id: str
    memory_type: MemoryType
    content: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    accessed_at: datetime = Field(default_factory=datetime.utcnow)
    relevance_score: float = 1.0
    embedding: Optional[List[float]] = None


class MemorySystem:
    """Advanced memory management system."""

    def __init__(self):
        self.memories: Dict[str, MemoryEntry] = {}
        self.agent_memories: Dict[str, List[str]] = {}

    def store_memory(self, agent_id: str, memory_type: MemoryType,
                    content: Dict[str, Any]) -> MemoryEntry:
        """Store a memory entry."""
        from uuid import uuid4
        memory_id = str(uuid4())
        entry = MemoryEntry(
            id=memory_id,
            agent_id=agent_id,
            memory_type=memory_type,
            content=content
        )
        self.memories[memory_id] = entry

        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = []
        self.agent_memories[agent_id].append(memory_id)

        return entry

    def retrieve_memory(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory."""
        if memory_id in self.memories:
            self.memories[memory_id].accessed_at = datetime.utcnow()
        return self.memories.get(memory_id)

    def get_agent_memories(self, agent_id: str,
                          memory_type: Optional[MemoryType] = None) -> List[MemoryEntry]:
        """Get all memories for an agent."""
        memory_ids = self.agent_memories.get(agent_id, [])
        memories = [self.memories[mid] for mid in memory_ids if mid in self.memories]

        if memory_type:
            memories = [m for m in memories if m.memory_type == memory_type]

        return sorted(memories, key=lambda m: m.accessed_at, reverse=True)

    def consolidate_memories(self, agent_id: str, memory_type: MemoryType) -> None:
        """Consolidate and optimize memories (placeholder for advanced consolidation)."""
        memories = self.get_agent_memories(agent_id, memory_type)
        for memory in memories:
            if len(memory.content) > 1000:
                memory.relevance_score *= 0.95

    def search_memories(self, agent_id: str, query: str) -> List[MemoryEntry]:
        """Search memories by keyword (placeholder for semantic search)."""
        memories = self.get_agent_memories(agent_id)
        query_lower = query.lower()

        results = []
        for memory in memories:
            content_str = str(memory.content).lower()
            if query_lower in content_str:
                results.append(memory)

        return sorted(results, key=lambda m: m.relevance_score, reverse=True)
