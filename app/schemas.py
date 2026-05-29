"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorldGenerationParams(BaseModel):
    """Parameters for world generation."""

    num_planets: int = Field(default=5, ge=1, le=100)
    num_civilizations: int = Field(default=10, ge=1, le=1000)
    technology_level: float = Field(default=1.0, ge=1.0, le=10.0)
    world_seed: Optional[int] = None


class WorldCreateRequest(BaseModel):
    """Request to create a new world."""

    name: str = Field(..., min_length=1, max_length=255)
    world_type: str = Field(default="normal")
    generation_params: WorldGenerationParams


class WorldResponse(BaseModel):
    """World data response."""

    id: str
    name: str
    world_type: str
    seed: int
    generation_status: str
    num_planets: int
    num_civilizations: int
    num_locations: int
    created_at: datetime
    updated_at: datetime
    last_simulated: Optional[datetime]

    class Config:
        from_attributes = True


class PlanetResponse(BaseModel):
    """Planet data response."""

    id: str
    world_id: str
    name: str
    terrain_type: str
    radius: float
    gravity: float
    temperature_avg: float
    humidity: float
    oxygen_level: float
    biomes: Dict[str, Any]
    resources: Dict[str, Any]
    habitable: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CivilizationResponse(BaseModel):
    """Civilization data response."""

    id: str
    world_id: str
    planet_id: Optional[str]
    name: str
    government_type: str
    stability: float
    population: int
    population_growth_rate: float
    wealth: float
    economic_output: float
    technology_level: float
    culture_description: Optional[str]
    values: Dict[str, Any]
    founding_year: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class LocationResponse(BaseModel):
    """Location data response."""

    id: str
    world_id: str
    planet_id: Optional[str]
    civilization_id: Optional[str]
    name: str
    location_type: str
    coordinates: Dict[str, Any]
    elevation: Optional[float]
    description: Optional[str]
    population: int
    discovered: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    """Event data response."""

    id: str
    world_id: str
    name: str
    description: str
    event_type: str
    severity: float
    world_year: int
    timestamp: datetime
    consequences: List[str]
    affected_entities: List[str]

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    database: str
    redis: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: Optional[str]
    timestamp: datetime
