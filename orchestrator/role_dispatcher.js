import fs from 'fs';
import { Logger } from './logger.js';

const logger = new Logger('orchestrator/role_dispatcher.js');

export class RoleDispatcher {
  constructor() {
    this.roleRegistry = this.loadRoleRegistry();
    this.assignmentHistory = [];
  }

  loadRoleRegistry() {
    try {
      const data = fs.readFileSync('./memory/agent_roles.json', 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      logger.error(`Failed to load role registry: ${error.message}`);
      return { role_categories: {} };
    }
  }

  assignRoles(tasks) {
    const assignments = [];

    for (const task of tasks) {
      const roles = this.selectRolesForTask(task);
      const assignment = {
        task_id: task.id,
        task_type: task.type,
        assigned_roles: roles,
        timestamp: new Date().toISOString()
      };

      assignments.push(assignment);
      this.assignmentHistory.push(assignment);
    }

    return assignments;
  }

  selectRolesForTask(task) {
    const categoryMap = {
      'climate_update': ['Climate Engineers'],
      'biome_evolution': ['Biome Architects'],
      'terrain_generation': ['Geology Specialists'],
      'city_development': ['City Planners'],
      'economy_simulation': ['Economy Managers'],
      'narrative_generation': ['Story Directors']
    };

    const roleCategory = categoryMap[task.type] || ['Earth Observers'];
    const roleCount = Math.min(2 + Math.floor(Math.random() * 2), 3);

    const selectedRoles = [];
    for (let i = 0; i < roleCount; i++) {
      const role = roleCategory[i % roleCategory.length];
      selectedRoles.push({
        name: role,
        assigned_id: `role_${Date.now()}_${i}`,
        capability: this.getCapabilityForRole(role)
      });
    }

    return selectedRoles;
  }

  getCapabilityForRole(roleName) {
    const capabilities = {
      'Climate Engineers': 'weather_generation',
      'Biome Architects': 'biome_design',
      'Geology Specialists': 'terrain_generation',
      'City Planners': 'city_design',
      'Economy Managers': 'economy_design',
      'Story Directors': 'story_generation',
      'Earth Observers': 'state_monitoring'
    };

    return capabilities[roleName] || 'general_task';
  }
}
