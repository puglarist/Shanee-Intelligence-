import axios from 'axios';
import { Logger } from '../orchestrator/logger.js';

const logger = new Logger('hf/integration.js');

export class HFIntegration {
  constructor() {
    this.mode = process.env.HF_MODE || 'mock';
    this.apiKey = process.env.HF_API_KEY || '';
    this.baseUrl = process.env.HF_BASE_URL || 'https://api-inference.huggingface.co';
    this.model = process.env.HF_MODEL || 'meta-llama/Llama-2-7b-hf';

    if (this.mode === 'production' && !this.apiKey) {
      logger.warn('HF_MODE is production but HF_API_KEY not set, falling back to mock mode');
      this.mode = 'mock';
    }

    logger.info(`HF Integration initialized in ${this.mode} mode`);
  }

  async processTasks(tasks, roleAssignments) {
    if (this.mode === 'mock') {
      return this.processMock(tasks, roleAssignments);
    } else {
      return this.processProduction(tasks, roleAssignments);
    }
  }

  processMock(tasks, roleAssignments) {
    const results = [];

    for (let i = 0; i < tasks.length; i++) {
      const task = tasks[i];
      const assignment = roleAssignments[i];

      const result = {
        task_id: task.id,
        task_type: task.type,
        assigned_roles: assignment.assigned_roles,
        status: 'completed',
        mock_execution: true,
        output: this.generateMockOutput(task),
        timestamp: new Date().toISOString()
      };

      results.push(result);
    }

    return results;
  }

  async processProduction(tasks, roleAssignments) {
    const results = [];

    for (let i = 0; i < tasks.length; i++) {
      const task = tasks[i];
      const assignment = roleAssignments[i];

      try {
        const prompt = this.buildPrompt(task, assignment);
        const hfResult = await this.callHFAPI(prompt);

        const result = {
          task_id: task.id,
          task_type: task.type,
          assigned_roles: assignment.assigned_roles,
          status: 'completed',
          hf_response: hfResult,
          output: this.parseHFOutput(hfResult),
          timestamp: new Date().toISOString()
        };

        results.push(result);
      } catch (error) {
        logger.error(`Failed to process task ${task.id}: ${error.message}`);
        results.push({
          task_id: task.id,
          status: 'failed',
          error: error.message,
          timestamp: new Date().toISOString()
        });
      }
    }

    return results;
  }

  buildPrompt(task, assignment) {
    const roles = assignment.assigned_roles.map(r => r.name).join(', ');
    return `Task: ${task.description}\nTask Type: ${task.type}\nAssigned Roles: ${roles}\nContext: ${JSON.stringify(task.context)}\n\nGenerate a detailed response for this task:`;
  }

  async callHFAPI(prompt) {
    try {
      const response = await axios.post(
        `${this.baseUrl}/models/${this.model}`,
        {
          inputs: prompt,
          parameters: {
            max_new_tokens: 256,
            temperature: 0.7
          }
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          },
          timeout: 30000
        }
      );

      return response.data;
    } catch (error) {
      logger.error(`HF API call failed: ${error.message}`);
      throw error;
    }
  }

  parseHFOutput(hfResponse) {
    if (Array.isArray(hfResponse) && hfResponse[0] && hfResponse[0].generated_text) {
      return {
        text: hfResponse[0].generated_text,
        parsed: true
      };
    }
    return { text: JSON.stringify(hfResponse), parsed: false };
  }

  generateMockOutput(task) {
    const mockOutputs = {
      'climate_update': {
        temperature_delta: (Math.random() - 0.5) * 0.2,
        pressure_change: (Math.random() - 0.5) * 5,
        co2_change: Math.random() * 2 - 1
      },
      'biome_evolution': {
        new_species_count: Math.floor(Math.random() * 5),
        ecosystem_health: 0.5 + Math.random() * 0.5,
        biome_changes: ['forest expansion', 'grassland shift', 'desert growth'][Math.floor(Math.random() * 3)]
      },
      'terrain_generation': {
        mountains_created: Math.floor(Math.random() * 3),
        elevation_change: Math.random() * 100 - 50,
        terrain_type: ['mountain', 'valley', 'plateau'][Math.floor(Math.random() * 3)]
      },
      'city_development': {
        population_growth: Math.floor(Math.random() * 1000),
        new_districts: Math.floor(Math.random() * 2),
        infrastructure_level: 0.5 + Math.random() * 0.5
      },
      'economy_simulation': {
        trade_volume: Math.random() * 1000,
        price_index: 100 + (Math.random() - 0.5) * 20,
        wealth_inequality: 0.3 + Math.random() * 0.4
      },
      'narrative_generation': {
        story_arc: ['rising action', 'climax', 'resolution'][Math.floor(Math.random() * 3)],
        event_importance: 0.5 + Math.random() * 0.5,
        narrative_impact: 'significant'
      }
    };

    return mockOutputs[task.type] || { status: 'executed', result: 'success' };
  }
}
