import fs from 'fs';
import path from 'path';
import { TaskGenerator } from './task_generator.js';
import { RoleDispatcher } from './role_dispatcher.js';
import { HFIntegration } from '../hf/integration.js';
import { EarthSimulation } from '../simulation/earth/generator.js';
import { Logger } from './logger.js';

const logger = new Logger('orchestrator/engine.js');
const ITERATION_INTERVAL = process.env.ITERATION_INTERVAL || 5000; // 5 seconds default

class OmniverseEngine {
  constructor() {
    this.iteration = 0;
    this.isRunning = false;
    this.taskGenerator = new TaskGenerator();
    this.roleDispatcher = new RoleDispatcher();
    this.hfIntegration = new HFIntegration();
    this.earthSimulation = new EarthSimulation();
    this.worldState = this.loadWorldState();
  }

  loadWorldState() {
    const statePath = './memory/world_state.json';
    try {
      const data = fs.readFileSync(statePath, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      logger.error(`Failed to load world state: ${error.message}`);
      return this.createDefaultState();
    }
  }

  createDefaultState() {
    return {
      timestamp: new Date().toISOString(),
      iteration: 0,
      status: 'initializing',
      earth: {
        age_cycles: 0,
        climate_state: { global_temperature: 15.2, sea_level: 0, atmospheric_co2: 420 },
        biomes: {},
        cities: [],
        regions: []
      },
      system_health: {
        orchestrator: 'running',
        hf_integration: 'ready',
        simulation: 'initialized',
        memory: 'active'
      },
      execution_metrics: {
        total_tasks_generated: 0,
        total_tasks_processed: 0,
        total_iterations: 0,
        last_update: new Date().toISOString()
      }
    };
  }

  async executeIteration() {
    try {
      this.iteration++;
      const timestamp = new Date().toISOString();
      logger.info(`\n=== ITERATION ${this.iteration} ===`);
      logger.info(`Timestamp: ${timestamp}`);

      // Step 1: Generate tasks
      logger.info('PHASE 1: Generating tasks...');
      const tasks = this.taskGenerator.generateTasks(this.worldState, 3 + Math.floor(Math.random() * 3));
      logger.info(`Generated ${tasks.length} tasks`);

      // Step 2: Dispatch roles
      logger.info('PHASE 2: Assigning roles...');
      const assignments = this.roleDispatcher.assignRoles(tasks);
      logger.info(`Assigned ${assignments.length} roles`);

      // Step 3: Process via HF
      logger.info('PHASE 3: Processing via HF/Mock...');
      const results = await this.hfIntegration.processTasks(tasks, assignments);
      logger.info(`Processed ${results.length} task results`);

      // Step 4: Earth simulation update
      logger.info('PHASE 4: Running Earth simulation...');
      const simulationUpdate = this.earthSimulation.step(this.worldState, results);
      logger.info(`Simulation state updated`);

      // Step 5: Update world state
      logger.info('PHASE 5: Updating world state...');
      this.updateWorldState(tasks, simulationUpdate);
      this.worldState.execution_metrics.total_iterations = this.iteration;

      // Step 6: Save state
      logger.info('PHASE 6: Persisting state...');
      this.saveWorldState();

      // Log summary
      logger.info(`Iteration ${this.iteration} complete`);
      logger.info(`Earth age: ${this.worldState.earth.age_cycles} cycles`);
      logger.info(`Cities: ${this.worldState.earth.cities.length}`);
      logger.info(`Temperature: ${this.worldState.earth.climate_state.global_temperature}°C`);
      logger.info('');

    } catch (error) {
      logger.error(`Iteration ${this.iteration} failed: ${error.message}`);
      console.error(error);
    }
  }

  updateWorldState(tasks, simulationUpdate) {
    this.worldState.timestamp = new Date().toISOString();
    this.worldState.iteration = this.iteration;
    this.worldState.execution_metrics.total_tasks_generated += tasks.length;
    this.worldState.execution_metrics.last_update = new Date().toISOString();

    if (simulationUpdate) {
      this.worldState.earth = {
        ...this.worldState.earth,
        ...simulationUpdate
      };
    }
  }

  saveWorldState() {
    try {
      const statePath = './memory/world_state.json';
      fs.writeFileSync(statePath, JSON.stringify(this.worldState, null, 2));
    } catch (error) {
      logger.error(`Failed to save world state: ${error.message}`);
    }
  }

  async start() {
    if (this.isRunning) {
      logger.warn('Engine already running');
      return;
    }

    this.isRunning = true;
    logger.info('🚀 Omniverse Engine starting...');
    logger.info(`Iteration interval: ${ITERATION_INTERVAL}ms`);
    logger.info('Running autonomous execution loop...');

    await this.executeIteration();

    this.intervalId = setInterval(() => {
      if (this.isRunning) {
        this.executeIteration();
      }
    }, ITERATION_INTERVAL);
  }

  stop() {
    this.isRunning = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    logger.info('⛔ Omniverse Engine stopped');
  }
}

// Main execution
const engine = new OmniverseEngine();

process.on('SIGINT', () => {
  logger.info('\nReceived SIGINT, shutting down...');
  engine.stop();
  process.exit(0);
});

process.on('SIGTERM', () => {
  logger.info('\nReceived SIGTERM, shutting down...');
  engine.stop();
  process.exit(0);
});

engine.start().catch(error => {
  logger.error(`Fatal error: ${error.message}`);
  process.exit(1);
});
