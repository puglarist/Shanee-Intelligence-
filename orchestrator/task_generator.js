import { Logger } from './logger.js';

const logger = new Logger('orchestrator/task_generator.js');

export class TaskGenerator {
  constructor() {
    this.taskTemplates = [
      // Earth simulation tasks
      {
        category: 'earth_simulation',
        type: 'climate_update',
        description: 'Update global climate state',
        subtasks: ['temperature_delta', 'pressure_change', 'co2_level']
      },
      {
        category: 'earth_simulation',
        type: 'biome_evolution',
        description: 'Evolve biomes and ecosystems',
        subtasks: ['species_generation', 'ecosystem_balance', 'resource_distribution']
      },
      {
        category: 'earth_simulation',
        type: 'terrain_generation',
        description: 'Generate or modify terrain features',
        subtasks: ['mountain_creation', 'valley_formation', 'elevation_mapping']
      },
      {
        category: 'civilization_systems',
        type: 'city_development',
        description: 'Develop city infrastructure and growth',
        subtasks: ['district_planning', 'infrastructure_building', 'population_growth']
      },
      {
        category: 'civilization_systems',
        type: 'economy_simulation',
        description: 'Simulate economic activity and trade',
        subtasks: ['resource_trading', 'price_fluctuation', 'wealth_distribution']
      },
      {
        category: 'cinematic_systems',
        type: 'narrative_generation',
        description: 'Generate world narrative and lore',
        subtasks: ['story_arc_creation', 'character_interaction', 'plot_development']
      }
    ];
  }

  generateTasks(worldState, count = 3) {
    const tasks = [];
    const earthAge = worldState.earth.age_cycles;

    for (let i = 0; i < count; i++) {
      const template = this.taskTemplates[Math.floor(Math.random() * this.taskTemplates.length)];
      const taskId = `task_${Date.now()}_${i}`;

      const task = {
        id: taskId,
        timestamp: new Date().toISOString(),
        category: template.category,
        type: template.type,
        description: template.description,
        subtasks: template.subtasks,
        priority: this.calculatePriority(template.category, earthAge),
        context: {
          world_age: earthAge,
          current_temperature: worldState.earth.climate_state.global_temperature,
          city_count: worldState.earth.cities.length,
          co2_level: worldState.earth.climate_state.atmospheric_co2
        },
        status: 'pending'
      };

      tasks.push(task);
    }

    return tasks;
  }

  calculatePriority(category, earthAge) {
    const priorities = {
      'earth_simulation': 1.0,
      'civilization_systems': earthAge > 10 ? 0.9 : 0.7,
      'cinematic_systems': earthAge > 5 ? 0.8 : 0.5,
      'stronghold_systems': 0.6
    };
    return priorities[category] || 0.5;
  }
}
