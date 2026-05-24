"""Memory Systems - Episodic, semantic, and procedural memory"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, List
from collections import defaultdict


@dataclass
class MemoryConfig:
    """Configuration for memory systems"""
    episodic_size: int = 1000
    semantic_size: int = 10000
    procedural_size: int = 500
    enable_consolidation: bool = True
    consolidation_interval_s: float = 3600.0


@dataclass
class EpisodeMemory:
    """Single episode/experience memory"""
    id: str
    timestamp: datetime
    content: str
    agent_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    importance: float = 1.0


@dataclass
class SemanticMemory:
    """Semantic knowledge (facts, concepts, relationships)"""
    id: str
    concept: str
    knowledge: str
    source: str
    confidence: float = 0.8
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProceduralMemory:
    """Skill/procedure memory"""
    id: str
    skill_name: str
    steps: List[str]
    success_rate: float = 0.0
    last_used: Optional[datetime] = None


class Memory(ABC):
    """Base class for memory implementations"""

    @abstractmethod
    async def store(self, memory: Any) -> str:
        """Store memory and return ID"""
        pass

    @abstractmethod
    async def retrieve(self, query: str) -> List[Any]:
        """Retrieve memories matching query"""
        pass

    @abstractmethod
    async def forget(self, memory_id: str) -> bool:
        """Remove memory"""
        pass


class EpisodicMemory(Memory):
    """
    Episodic memory: experiences and events.
    Like human autobiographical memory.
    """

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.memories: dict[str, EpisodeMemory] = {}
        self.timeline: list[str] = []

    async def store(self, memory: EpisodeMemory) -> str:
        """Store episode"""
        self.memories[memory.id] = memory
        self.timeline.append(memory.id)

        if len(self.memories) > self.max_size:
            oldest = self.timeline.pop(0)
            del self.memories[oldest]

        return memory.id

    async def retrieve(self, query: str) -> list[EpisodeMemory]:
        """Retrieve episodes by content match"""
        query_lower = query.lower()
        results = [m for m in self.memories.values()
                  if query_lower in m.content.lower()]
        return sorted(results, key=lambda x: x.timestamp, reverse=True)

    async def retrieve_recent(self, count: int = 5) -> list[EpisodeMemory]:
        """Get most recent episodes"""
        recent_ids = self.timeline[-count:]
        return [self.memories[id] for id in recent_ids]

    async def forget(self, memory_id: str) -> bool:
        """Remove episode"""
        if memory_id in self.memories:
            del self.memories[memory_id]
            self.timeline.remove(memory_id)
            return True
        return False


class SemanticMemoryStore(Memory):
    """
    Semantic memory: facts and knowledge.
    Like human conceptual knowledge.
    """

    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.memories: dict[str, SemanticMemory] = {}
        self.concept_index: dict[str, list[str]] = defaultdict(list)

    async def store(self, memory: SemanticMemory) -> str:
        """Store semantic knowledge"""
        self.memories[memory.id] = memory
        self.concept_index[memory.concept.lower()].append(memory.id)

        if len(self.memories) > self.max_size:
            oldest = min(self.memories.values(),
                        key=lambda x: x.created_at)
            await self.forget(oldest.id)

        return memory.id

    async def retrieve(self, query: str) -> list[SemanticMemory]:
        """Retrieve knowledge about concept"""
        query_lower = query.lower()
        memory_ids = self.concept_index.get(query_lower, [])
        results = [self.memories[id] for id in memory_ids
                  if id in self.memories]
        return sorted(results, key=lambda x: x.confidence, reverse=True)

    async def forget(self, memory_id: str) -> bool:
        """Remove semantic knowledge"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            concept = memory.concept.lower()
            if memory_id in self.concept_index[concept]:
                self.concept_index[concept].remove(memory_id)
            del self.memories[memory_id]
            return True
        return False


class ProceduralMemoryStore(Memory):
    """
    Procedural memory: skills and how-tos.
    Like human motor/procedural memory.
    """

    def __init__(self, max_size: int = 500):
        self.max_size = max_size
        self.memories: dict[str, ProceduralMemory] = {}
        self.skill_index: dict[str, list[str]] = defaultdict(list)

    async def store(self, memory: ProceduralMemory) -> str:
        """Store skill/procedure"""
        self.memories[memory.id] = memory
        self.skill_index[memory.skill_name.lower()].append(memory.id)

        if len(self.memories) > self.max_size:
            least_used = min(
                self.memories.values(),
                key=lambda x: x.success_rate
            )
            await self.forget(least_used.id)

        return memory.id

    async def retrieve(self, query: str) -> list[ProceduralMemory]:
        """Retrieve skills matching query"""
        query_lower = query.lower()
        memory_ids = self.skill_index.get(query_lower, [])
        results = [self.memories[id] for id in memory_ids
                  if id in self.memories]
        return sorted(results, key=lambda x: x.success_rate, reverse=True)

    async def forget(self, memory_id: str) -> bool:
        """Remove skill memory"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            skill = memory.skill_name.lower()
            if memory_id in self.skill_index[skill]:
                self.skill_index[skill].remove(memory_id)
            del self.memories[memory_id]
            return True
        return False


class MemoryController:
    """
    Unified controller for all memory systems.
    Coordinates storage and retrieval.
    """

    def __init__(self, config: MemoryConfig):
        self.config = config
        self.episodic = EpisodicMemory(config.episodic_size)
        self.semantic = SemanticMemoryStore(config.semantic_size)
        self.procedural = ProceduralMemoryStore(config.procedural_size)

    async def store_episode(self, episode: EpisodeMemory) -> str:
        """Store experience"""
        return await self.episodic.store(episode)

    async def store_knowledge(self, knowledge: SemanticMemory) -> str:
        """Store semantic knowledge"""
        return await self.semantic.store(knowledge)

    async def store_skill(self, skill: ProceduralMemory) -> str:
        """Store skill/procedure"""
        return await self.procedural.store(skill)

    async def recall(self, query: str, memory_type: Optional[str] = None) -> dict:
        """Unified recall across memory systems"""
        results = {}

        if memory_type in [None, "episodic"]:
            results["episodic"] = await self.episodic.retrieve(query)

        if memory_type in [None, "semantic"]:
            results["semantic"] = await self.semantic.retrieve(query)

        if memory_type in [None, "procedural"]:
            results["procedural"] = await self.procedural.retrieve(query)

        return results

    async def consolidate(self):
        """Consolidate memories (e.g., extract semantics from episodes)"""
        if not self.config.enable_consolidation:
            return

        # Move frequently used episodes to semantic knowledge
        # Extract skills from successful procedural memories
        pass
