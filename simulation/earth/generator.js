import { Logger } from '../../orchestrator/logger.js';

const logger = new Logger('simulation/earth/generator.js');

export class EarthSimulation {
  constructor() {
    this.constants = {
      MAX_TEMPERATURE: 60,
      MIN_TEMPERATURE: -50,
      TEMPERATURE_CHANGE_RATE: 0.1,
      CO2_INCREASE_RATE: 0.5,
      SEA_LEVEL_CHANGE_RATE: 0.01
    };
    this.cityCounter = 0;
  }

  step(worldState, taskResults) {
    const earthState = worldState.earth;
    const update = {
      age_cycles: earthState.age_cycles + 1,
      climate_state: this.updateClimate(earthState.climate_state, taskResults),
      biomes: this.updateBiomes(earthState.biomes, taskResults),
      cities: this.updateCities(earthState.cities, taskResults),
      regions: this.updateRegions(earthState.regions, taskResults)
    };

    logger.info(`Earth simulation step: age=${update.age_cycles}, temp=${update.climate_state.global_temperature.toFixed(2)}°C`);
    return update;
  }

  updateClimate(climateState, taskResults) {
    let tempDelta = 0;
    let co2Delta = 0;
    let seaLevelDelta = 0;

    // Process task results for climate impacts
    for (const result of taskResults) {
      if (result.status === 'completed' && result.output) {
        const output = result.output;

        if (result.task_type === 'climate_update') {
          tempDelta += output.temperature_delta || 0;
          co2Delta += output.co2_change || 0;
        } else if (result.task_type === 'biome_evolution') {
          // Biome evolution affects CO2
          co2Delta += output.ecosystem_health ? -0.5 : 0.5;
        }
      }
    }

    // Apply constraints
    let newTemp = climateState.global_temperature + tempDelta;
    newTemp = Math.max(this.constants.MIN_TEMPERATURE, Math.min(this.constants.MAX_TEMPERATURE, newTemp));

    let newCO2 = climateState.atmospheric_co2 + co2Delta + (Math.random() - 0.5) * this.constants.CO2_INCREASE_RATE;
    newCO2 = Math.max(280, newCO2); // Pre-industrial baseline

    let newSeaLevel = climateState.sea_level + seaLevelDelta + (Math.random() - 0.5) * this.constants.SEA_LEVEL_CHANGE_RATE;

    return {
      global_temperature: parseFloat(newTemp.toFixed(2)),
      sea_level: parseFloat(newSeaLevel.toFixed(2)),
      atmospheric_co2: parseFloat(newCO2.toFixed(1))
    };
  }

  updateBiomes(biomes, taskResults) {
    const updatedBiomes = { ...biomes };

    for (const result of taskResults) {
      if (result.task_type === 'biome_evolution' && result.output) {
        const { new_species_count, ecosystem_health, biome_changes } = result.output;
        const biomeKey = biome_changes || 'forest';

        if (!updatedBiomes[biomeKey]) {
          updatedBiomes[biomeKey] = {
            name: biomeKey,
            species_count: 0,
            health: 0.5,
            area: 0,
            created_at: new Date().toISOString()
          };
        }

        updatedBiomes[biomeKey].species_count += new_species_count || 0;
        updatedBiomes[biomeKey].health = Math.min(1, ecosystem_health || updatedBiomes[biomeKey].health);
        updatedBiomes[biomeKey].area += Math.random() * 100;
      }
    }

    return updatedBiomes;
  }

  updateCities(cities, taskResults) {
    let updatedCities = [...cities];

    for (const result of taskResults) {
      if (result.task_type === 'city_development' && result.output) {
        const { population_growth, new_districts, infrastructure_level } = result.output;

        if (new_districts > 0 && updatedCities.length === 0) {
          // Create first city
          const newCity = {
            id: `city_${++this.cityCounter}`,
            name: this.generateCityName(),
            population: 10000 + population_growth,
            districts: new_districts,
            infrastructure: infrastructure_level,
            created_at: new Date().toISOString(),
            coordinates: {
              x: Math.random() * 1000,
              y: Math.random() * 1000
            }
          };
          updatedCities.push(newCity);
          logger.info(`Created new city: ${newCity.name} (pop: ${newCity.population})`);
        } else if (updatedCities.length > 0) {
          // Grow existing cities
          updatedCities = updatedCities.map(city => ({
            ...city,
            population: city.population + population_growth,
            districts: city.districts + new_districts,
            infrastructure: Math.min(1, city.infrastructure + 0.05)
          }));
        }
      }
    }

    return updatedCities;
  }

  updateRegions(regions, taskResults) {
    let updatedRegions = [...regions];

    for (const result of taskResults) {
      if (result.task_type === 'terrain_generation' && result.output) {
        const { mountains_created, elevation_change, terrain_type } = result.output;

        if (mountains_created > 0) {
          const region = {
            id: `region_${Date.now()}`,
            type: terrain_type,
            elevation: elevation_change,
            mountains: mountains_created,
            area: Math.random() * 500,
            created_at: new Date().toISOString()
          };
          updatedRegions.push(region);
        }
      }
    }

    return updatedRegions;
  }

  generateCityName() {
    const prefixes = ['New', 'Old', 'Great', 'Rising'];
    const suffixes = ['Haven', 'Harbor', 'Peak', 'Springs', 'Field', 'Vale'];
    const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
    const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
    return `${prefix} ${suffix}`;
  }
}
