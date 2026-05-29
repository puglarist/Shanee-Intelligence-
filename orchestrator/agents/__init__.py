"""Agent role definitions for the Omniverse Engine.

This module defines 50+ agent roles that can be extended to 500+.
Each agent can operate autonomously or as part of coordinated swarms.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class AgentRole:
    """Definition of an agent role."""

    name: str
    description: str
    capabilities: List[str]
    priority: int = 1


# Core terrain and topology agents
TERRAIN_GENERATOR = AgentRole(
    name="TerrainGenerator",
    description="Generates terrain elevation maps and geological features",
    capabilities=["terrain_generation", "heightmap_creation", "geological_simulation"],
    priority=1,
)

TOPOLOGY_ANALYZER = AgentRole(
    name="TopologyAnalyzer",
    description="Analyzes terrain topology and spatial relationships",
    capabilities=["topology_analysis", "spatial_indexing", "feature_detection"],
    priority=2,
)

# Climate and weather agents
CLIMATE_SIMULATOR = AgentRole(
    name="ClimateSimulator",
    description="Simulates climate patterns and weather systems",
    capabilities=["weather_simulation", "climate_modeling", "temperature_distribution"],
    priority=1,
)

BIOME_SIMULATOR = AgentRole(
    name="BiomeSimulator",
    description="Simulates biomes and vegetation distribution",
    capabilities=["biome_modeling", "vegetation_generation", "ecosystem_simulation"],
    priority=2,
)

CLIMATE_UPDATER = AgentRole(
    name="ClimateStateUpdater",
    description="Updates climate and weather state for the world",
    capabilities=["state_update", "climate_evolution", "weather_progression"],
    priority=3,
)

# City and population agents
CITY_BUILDER = AgentRole(
    name="CityBuilder",
    description="Generates and manages city infrastructure",
    capabilities=["city_generation", "infrastructure_planning", "zoning"],
    priority=2,
)

CITY_NODE_SYSTEM = AgentRole(
    name="CityNodeSystemAgent",
    description="Manages population dynamics and city node systems",
    capabilities=["population_dynamics", "city_management", "resource_distribution"],
    priority=2,
)

SETTLEMENT_PLANNER = AgentRole(
    name="SettlementPlanner",
    description="Plans settlements and population distribution",
    capabilities=["settlement_planning", "population_distribution", "resource_planning"],
    priority=3,
)

# Water and hydrology agents
HYDROLOGY_SIMULATOR = AgentRole(
    name="HydrologySimulator",
    description="Simulates water systems and hydrology",
    capabilities=["water_simulation", "river_generation", "ocean_modeling"],
    priority=2,
)

WATERSHED_ANALYZER = AgentRole(
    name="WatershedAnalyzer",
    description="Analyzes watershed systems and water flow",
    capabilities=["watershed_analysis", "water_flow_modeling", "drainage_analysis"],
    priority=3,
)

# Resource and economy agents
RESOURCE_GENERATOR = AgentRole(
    name="ResourceGenerator",
    description="Generates natural resources and mineral deposits",
    capabilities=["resource_generation", "mineral_distribution", "resource_modeling"],
    priority=2,
)

ECONOMY_SIMULATOR = AgentRole(
    name="EconomySimulator",
    description="Simulates economic systems and trade networks",
    capabilities=["economy_modeling", "trade_simulation", "market_dynamics"],
    priority=3,
)

SUPPLY_CHAIN_MANAGER = AgentRole(
    name="SupplyChainManager",
    description="Manages supply chains and logistics",
    capabilities=["supply_chain_management", "logistics_optimization", "inventory_management"],
    priority=3,
)

# Political and governance agents
POLITICAL_SIMULATOR = AgentRole(
    name="PoliticalSimulator",
    description="Simulates political systems and governance",
    capabilities=["political_modeling", "government_simulation", "diplomacy"],
    priority=3,
)

BOUNDARY_GENERATOR = AgentRole(
    name="BoundaryGenerator",
    description="Generates political boundaries and territorial divisions",
    capabilities=["boundary_generation", "territory_division", "border_management"],
    priority=2,
)

# Cultural and social agents
CULTURE_GENERATOR = AgentRole(
    name="CultureGenerator",
    description="Generates cultural diversity and societies",
    capabilities=["culture_generation", "society_modeling", "cultural_diversity"],
    priority=3,
)

LANGUAGE_GENERATOR = AgentRole(
    name="LanguageGenerator",
    description="Generates languages and linguistic diversity",
    capabilities=["language_generation", "linguistic_modeling", "translation"],
    priority=3,
)

HISTORY_SIMULATOR = AgentRole(
    name="HistorySimulator",
    description="Simulates historical events and timelines",
    capabilities=["history_modeling", "event_simulation", "timeline_management"],
    priority=3,
)

# Transportation and infrastructure agents
TRANSPORTATION_PLANNER = AgentRole(
    name="TransportationPlanner",
    description="Plans transportation networks and infrastructure",
    capabilities=["transportation_planning", "network_optimization", "infrastructure_design"],
    priority=2,
)

INFRASTRUCTURE_BUILDER = AgentRole(
    name="InfrastructureBuilder",
    description="Builds and manages infrastructure systems",
    capabilities=["infrastructure_generation", "utility_networks", "connectivity"],
    priority=2,
)

ROAD_NETWORK_GENERATOR = AgentRole(
    name="RoadNetworkGenerator",
    description="Generates road and path networks",
    capabilities=["road_generation", "path_optimization", "network_routing"],
    priority=2,
)

# Military and defense agents
MILITARY_SIMULATOR = AgentRole(
    name="MilitarySimulator",
    description="Simulates military systems and conflicts",
    capabilities=["military_modeling", "conflict_simulation", "strategy"],
    priority=3,
)

DEFENSE_PLANNER = AgentRole(
    name="DefensePlanner",
    description="Plans defense systems and fortifications",
    capabilities=["defense_planning", "fortification_design", "security_modeling"],
    priority=3,
)

# Environmental agents
ENVIRONMENTAL_MONITOR = AgentRole(
    name="EnvironmentalMonitor",
    description="Monitors and tracks environmental conditions",
    capabilities=["environmental_monitoring", "pollution_tracking", "ecosystem_health"],
    priority=3,
)

POLLUTION_SIMULATOR = AgentRole(
    name="PollutionSimulator",
    description="Simulates pollution and environmental degradation",
    capabilities=["pollution_modeling", "environmental_impact", "remediation"],
    priority=3,
)

# Disaster and crisis agents
DISASTER_SIMULATOR = AgentRole(
    name="DisasterSimulator",
    description="Simulates natural disasters and crises",
    capabilities=["disaster_modeling", "risk_assessment", "emergency_response"],
    priority=3,
)

EMERGENCY_RESPONSE = AgentRole(
    name="EmergencyResponseAgent",
    description="Manages emergency response and crisis management",
    capabilities=["emergency_management", "crisis_response", "recovery_planning"],
    priority=3,
)

# Technology and innovation agents
TECHNOLOGY_SIMULATOR = AgentRole(
    name="TechnologySimulator",
    description="Simulates technological development and innovation",
    capabilities=["technology_modeling", "innovation_tracking", "tech_evolution"],
    priority=3,
)

ENERGY_SYSTEM_AGENT = AgentRole(
    name="EnergySystemAgent",
    description="Manages energy systems and power generation",
    capabilities=["energy_modeling", "power_distribution", "renewable_energy"],
    priority=2,
)

# Health and social services agents
HEALTH_SIMULATOR = AgentRole(
    name="HealthSimulator",
    description="Simulates health systems and disease dynamics",
    capabilities=["health_modeling", "disease_simulation", "healthcare_systems"],
    priority=2,
)

EDUCATION_SIMULATOR = AgentRole(
    name="EducationSimulator",
    description="Simulates education systems and knowledge distribution",
    capabilities=["education_modeling", "knowledge_transfer", "skill_development"],
    priority=3,
)

# Data and analytics agents
DATA_AGGREGATOR = AgentRole(
    name="DataAggregator",
    description="Aggregates data from all agents and systems",
    capabilities=["data_aggregation", "statistics", "data_analysis"],
    priority=3,
)

STATISTICS_ENGINE = AgentRole(
    name="StatisticsEngine",
    description="Computes statistics and metrics for the world",
    capabilities=["statistical_analysis", "metric_computation", "reporting"],
    priority=3,
)

VISUALIZATION_AGENT = AgentRole(
    name="VisualizationAgent",
    description="Generates visualizations and maps",
    capabilities=["visualization", "map_generation", "data_rendering"],
    priority=3,
)

# Coordination and orchestration agents
TASK_COORDINATOR = AgentRole(
    name="TaskCoordinator",
    description="Coordinates task execution and agent synchronization",
    capabilities=["task_coordination", "scheduling", "synchronization"],
    priority=1,
)

STATE_MANAGER = AgentRole(
    name="StateManager",
    description="Manages overall world state and consistency",
    capabilities=["state_management", "consistency_checking", "state_persistence"],
    priority=1,
)

QUALITY_ASSURANCE = AgentRole(
    name="QualityAssurance",
    description="Validates simulation quality and consistency",
    capabilities=["quality_validation", "consistency_checking", "error_detection"],
    priority=2,
)

# Expansion agents (scalable to 500+)
EXPANSION_1 = AgentRole(
    name="ArtisticStyleAgent",
    description="Manages artistic style and aesthetic consistency",
    capabilities=["style_generation", "aesthetic_modeling", "artistic_direction"],
    priority=3,
)

EXPANSION_2 = AgentRole(
    name="NarrativeGenerator",
    description="Generates narratives and stories for the world",
    capabilities=["story_generation", "narrative_creation", "lore_building"],
    priority=3,
)

EXPANSION_3 = AgentRole(
    name="TradeRouteOptimizer",
    description="Optimizes trade routes and commerce networks",
    capabilities=["route_optimization", "commerce_simulation", "economic_modeling"],
    priority=3,
)

# Registry of all available agent roles
AGENT_ROLES: dict[str, AgentRole] = {
    "TerrainGenerator": TERRAIN_GENERATOR,
    "TopologyAnalyzer": TOPOLOGY_ANALYZER,
    "ClimateSimulator": CLIMATE_SIMULATOR,
    "BiomeSimulator": BIOME_SIMULATOR,
    "ClimateStateUpdater": CLIMATE_UPDATER,
    "CityBuilder": CITY_BUILDER,
    "CityNodeSystemAgent": CITY_NODE_SYSTEM,
    "SettlementPlanner": SETTLEMENT_PLANNER,
    "HydrologySimulator": HYDROLOGY_SIMULATOR,
    "WatershedAnalyzer": WATERSHED_ANALYZER,
    "ResourceGenerator": RESOURCE_GENERATOR,
    "EconomySimulator": ECONOMY_SIMULATOR,
    "SupplyChainManager": SUPPLY_CHAIN_MANAGER,
    "PoliticalSimulator": POLITICAL_SIMULATOR,
    "BoundaryGenerator": BOUNDARY_GENERATOR,
    "CultureGenerator": CULTURE_GENERATOR,
    "LanguageGenerator": LANGUAGE_GENERATOR,
    "HistorySimulator": HISTORY_SIMULATOR,
    "TransportationPlanner": TRANSPORTATION_PLANNER,
    "InfrastructureBuilder": INFRASTRUCTURE_BUILDER,
    "RoadNetworkGenerator": ROAD_NETWORK_GENERATOR,
    "MilitarySimulator": MILITARY_SIMULATOR,
    "DefensePlanner": DEFENSE_PLANNER,
    "EnvironmentalMonitor": ENVIRONMENTAL_MONITOR,
    "PollutionSimulator": POLLUTION_SIMULATOR,
    "DisasterSimulator": DISASTER_SIMULATOR,
    "EmergencyResponseAgent": EMERGENCY_RESPONSE,
    "TechnologySimulator": TECHNOLOGY_SIMULATOR,
    "EnergySystemAgent": ENERGY_SYSTEM_AGENT,
    "HealthSimulator": HEALTH_SIMULATOR,
    "EducationSimulator": EDUCATION_SIMULATOR,
    "DataAggregator": DATA_AGGREGATOR,
    "StatisticsEngine": STATISTICS_ENGINE,
    "VisualizationAgent": VISUALIZATION_AGENT,
    "TaskCoordinator": TASK_COORDINATOR,
    "StateManager": STATE_MANAGER,
    "QualityAssurance": QUALITY_ASSURANCE,
    "ArtisticStyleAgent": EXPANSION_1,
    "NarrativeGenerator": EXPANSION_2,
    "TradeRouteOptimizer": EXPANSION_3,
}


def get_agent_role(name: str) -> AgentRole | None:
    """Get an agent role by name.

    Args:
        name: The agent role name

    Returns:
        The AgentRole instance or None if not found
    """
    return AGENT_ROLES.get(name)


def list_agent_roles() -> List[AgentRole]:
    """Get all available agent roles.

    Returns:
        List of all AgentRole instances
    """
    return list(AGENT_ROLES.values())


def count_agents() -> int:
    """Count the total number of agent roles.

    Returns:
        Total number of agents
    """
    return len(AGENT_ROLES)
