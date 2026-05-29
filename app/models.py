"""SQLAlchemy database models."""

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship
import enum

from app.db import Base


class WorldType(str, enum.Enum):
    """Type of world."""

    NORMAL = "normal"
    STRONGHOLD = "stronghold"


class GovernmentType(str, enum.Enum):
    """Types of governments."""

    MONARCHY = "monarchy"
    DEMOCRACY = "democracy"
    THEOCRACY = "theocracy"
    OLIGARCHY = "oligarchy"
    AUTOCRACY = "autocracy"
    FEDERATION = "federation"
    CONFEDERACY = "confederacy"
    ANARCHY = "anarchy"


class World(Base):
    """Represents a generated world/universe."""

    __tablename__ = "worlds"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    world_type = Column(Enum(WorldType), default=WorldType.NORMAL)
    seed = Column(Integer, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_simulated = Column(DateTime, nullable=True)

    # Generation parameters
    generation_params = Column(JSON, nullable=False)  # Stores generation config
    generation_status = Column(String(50), default="pending")  # pending, generating, complete, failed

    # World statistics
    num_planets = Column(Integer, default=0)
    num_civilizations = Column(Integer, default=0)
    num_locations = Column(Integer, default=0)

    # Relationships
    planets = relationship("Planet", back_populates="world", cascade="all, delete-orphan")
    civilizations = relationship("Civilization", back_populates="world", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="world", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="world", cascade="all, delete-orphan")
    agent_memories = relationship("AgentMemory", back_populates="world", cascade="all, delete-orphan")


class Planet(Base):
    """Represents a planet in a world."""

    __tablename__ = "planets"

    id = Column(String, primary_key=True)
    world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    name = Column(String(255), nullable=False)

    # Terrain and geography
    terrain_type = Column(String(50), nullable=False)  # terrestrial, gas_giant, ice, desert, etc.
    radius = Column(Float, nullable=False)
    gravity = Column(Float, nullable=False)

    # Climate
    temperature_avg = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)  # 0-100
    oxygen_level = Column(Float, nullable=False)  # 0-100

    # Biomes (stored as JSON array)
    biomes = Column(JSON, nullable=False)

    # Resources
    resources = Column(JSON, nullable=False)  # {resource_type: quantity}

    # Metadata
    habitable = Column(Integer, default=0)  # boolean: 0 or 1
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    world = relationship("World", back_populates="planets")
    locations = relationship("Location", back_populates="planet", cascade="all, delete-orphan")


class Civilization(Base):
    """Represents a civilization on a planet."""

    __tablename__ = "civilizations"

    id = Column(String, primary_key=True)
    world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    planet_id = Column(String, ForeignKey("planets.id"), nullable=True)
    name = Column(String(255), nullable=False)

    # Government and politics
    government_type = Column(Enum(GovernmentType), nullable=False)
    stability = Column(Float, default=0.5)  # 0-1, 0=unstable, 1=stable

    # Population and demographics
    population = Column(Integer, default=0)
    population_growth_rate = Column(Float, default=0.02)  # annual

    # Economy
    wealth = Column(Float, default=1000)
    economic_output = Column(Float, default=100)
    trade_routes = Column(JSON, default={})  # {civ_id: quantity}

    # Culture
    culture_description = Column(Text, nullable=True)
    values = Column(JSON, default={})  # {value_name: strength}
    technology_level = Column(Float, default=1.0)  # 1-10

    # History
    founding_year = Column(Integer, nullable=True)
    history = Column(Text, nullable=True)
    conflicts = Column(JSON, default=[])  # List of conflict descriptions

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    world = relationship("World", back_populates="civilizations")
    locations = relationship("Location", back_populates="civilization")
    npcs = relationship("NPC", back_populates="civilization", cascade="all, delete-orphan")


class Location(Base):
    """Represents a location (city, landmark, dungeon, etc.)."""

    __tablename__ = "locations"

    id = Column(String, primary_key=True)
    world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    planet_id = Column(String, ForeignKey("planets.id"), nullable=True)
    civilization_id = Column(String, ForeignKey("civilizations.id"), nullable=True)

    name = Column(String(255), nullable=False)
    location_type = Column(String(50), nullable=False)  # city, village, dungeon, ruin, landmark

    # Geography
    coordinates = Column(JSON, nullable=False)  # {x, y, z}
    elevation = Column(Float, nullable=True)

    # Description
    description = Column(Text, nullable=True)
    districts = Column(JSON, default=[])  # For cities: list of districts with their properties
    landmarks = Column(JSON, default=[])  # Points of interest

    # Population
    population = Column(Integer, default=0)
    governance = Column(String(50), nullable=True)

    # Metadata
    discovered = Column(Integer, default=0)  # boolean
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    world = relationship("World", back_populates="locations")
    planet = relationship("Planet", back_populates="locations")
    civilization = relationship("Civilization", back_populates="locations")


class NPC(Base):
    """Represents a non-player character."""

    __tablename__ = "npcs"

    id = Column(String, primary_key=True)
    civilization_id = Column(String, ForeignKey("civilizations.id"), nullable=False)
    name = Column(String(255), nullable=False)

    # Personality
    personality_traits = Column(JSON, default={})  # {trait: strength}
    motivations = Column(JSON, default=[])  # List of motivations
    beliefs = Column(JSON, default=[])  # List of beliefs

    # Relationships
    relationships = Column(JSON, default={})  # {npc_id: relationship_type}

    # Role
    role = Column(String(100), nullable=True)  # ruler, merchant, scholar, warrior, etc.
    faction = Column(String(100), nullable=True)

    # Dialogue and knowledge
    dialogue_topics = Column(JSON, default=[])
    known_locations = Column(JSON, default=[])

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    civilization = relationship("Civilization", back_populates="npcs")


class Event(Base):
    """Represents a generated event in world history."""

    __tablename__ = "events"

    id = Column(String, primary_key=True)
    world_id = Column(String, ForeignKey("worlds.id"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # Event classification
    event_type = Column(String(50), nullable=False)  # war, discovery, disaster, social, etc.
    severity = Column(Float, default=0.5)  # 0-1

    # Temporal
    world_year = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Consequences
    consequences = Column(JSON, default=[])
    affected_entities = Column(JSON, default=[])  # List of affected civ/location IDs

    # Metadata
    generated_by_agent = Column(String(100), nullable=True)  # Agent ID that generated event

    # Relationships
    world = relationship("World", back_populates="events")


class AgentMemory(Base):
    """Stores semantic memory for AI agents."""

    __tablename__ = "agent_memories"

    id = Column(String, primary_key=True)
    world_id = Column(String, ForeignKey("worlds.id"), nullable=False)

    agent_id = Column(String, nullable=False)  # Agent identifier
    memory_type = Column(String(50), nullable=False)  # decision, observation, learning, etc.

    # Content
    content = Column(Text, nullable=False)  # The memory text
    embedding = Column(JSON, nullable=True)  # Vector embedding for similarity search

    # Context
    context = Column(JSON, default={})  # Additional metadata about the memory
    importance = Column(Float, default=0.5)  # 0-1, how important is this memory

    # Temporal
    created_at = Column(DateTime, default=datetime.utcnow)
    accessed_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    world = relationship("World", back_populates="agent_memories")


class StrongholdState(Base):
    """Maintains the state of the Stronghold protected world."""

    __tablename__ = "stronghold_state"

    id = Column(String, primary_key=True, default="primary")
    world_id = Column(String, ForeignKey("worlds.id"), nullable=False)

    # Infrastructure status
    defense_level = Column(Float, default=1.0)  # 0-1
    resource_reserves = Column(JSON, default={})  # {resource: quantity}

    # Systems status
    healing_system_active = Column(Integer, default=1)  # boolean
    backup_system_active = Column(Integer, default=1)  # boolean

    # Governance
    ai_governance_policy = Column(JSON, default={})
    access_control = Column(JSON, default={})  # {role: permissions}

    # Districts
    districts_status = Column(JSON, default={})  # {district_id: status}

    # Metadata
    last_backup = Column(DateTime, nullable=True)
    last_integrity_check = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    world = relationship("World", foreign_keys=[world_id])
