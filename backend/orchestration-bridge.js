/**
 * Orchestration Bridge
 * Handles communication between Express backend and FastAPI orchestrator
 * Manages task synchronization, world state updates, and agent coordination
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const debug = require('debug')('omniverse:orchestration-bridge');

/**
 * Initialize orchestration bridge routes
 * @param {Object} db - Database instance
 * @returns {Router} Express router with orchestration endpoints
 */
function initOrchestrationBridge(db) {
  const router = express.Router();

  // Memory folder paths
  const MEMORY_DIR = path.join(__dirname, '..', 'memory');
  const WORLD_STATE_FILE = path.join(MEMORY_DIR, 'world_state.json');
  const TASKS_QUEUE_FILE = path.join(MEMORY_DIR, 'tasks_queue.json');
  const AGENTS_FILE = path.join(MEMORY_DIR, 'agents.json');

  // Ensure memory directory exists
  function ensureMemoryDir() {
    if (!fs.existsSync(MEMORY_DIR)) {
      fs.mkdirSync(MEMORY_DIR, { recursive: true });
    }
  }

  /**
   * GET /api/sync/tasks - Fetch pending tasks from orchestrator
   * Returns tasks that need to be executed
   */
  router.get('/tasks', (req, res) => {
    try {
      ensureMemoryDir();

      let tasks = [];

      // Try to read from memory file first
      if (fs.existsSync(TASKS_QUEUE_FILE)) {
        const content = fs.readFileSync(TASKS_QUEUE_FILE, 'utf8');
        const data = JSON.parse(content);
        tasks = data.queue || [];
      }

      debug(`Fetched ${tasks.length} pending tasks`);
      res.json({
        status: 'success',
        tasks: tasks,
        count: tasks.length,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      debug('Error fetching tasks:', error);
      res.status(500).json({
        status: 'error',
        message: error.message,
      });
    }
  });

  /**
   * POST /api/sync/state - Receive world state updates from orchestrator
   * Processes and stores world state changes
   */
  router.post('/state', (req, res) => {
    try {
      ensureMemoryDir();

      const worldState = req.body;

      // Validate world state has required fields
      if (!worldState || typeof worldState !== 'object') {
        return res.status(400).json({
          status: 'error',
          message: 'Invalid world state object',
        });
      }

      // Write to memory file
      fs.writeFileSync(
        WORLD_STATE_FILE,
        JSON.stringify(
          {
            state: worldState,
            timestamp: new Date().toISOString(),
            version: Date.now(),
          },
          null,
          2
        )
      );

      // Also persist to database if available
      if (db && db.updateWorldState) {
        db.updateWorldState(worldState);
      }

      debug('World state updated successfully');
      res.json({
        status: 'success',
        message: 'World state updated',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      debug('Error updating world state:', error);
      res.status(500).json({
        status: 'error',
        message: error.message,
      });
    }
  });

  /**
   * GET /api/sync/state - Get current world state
   * Returns the latest world state snapshot
   */
  router.get('/state', (req, res) => {
    try {
      ensureMemoryDir();

      let state = null;
      let version = 0;

      // Try to read from memory file
      if (fs.existsSync(WORLD_STATE_FILE)) {
        const content = fs.readFileSync(WORLD_STATE_FILE, 'utf8');
        const data = JSON.parse(content);
        state = data.state;
        version = data.version || 0;
      }

      debug('World state retrieved, version:', version);
      res.json({
        status: 'success',
        state: state,
        version: version,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      debug('Error retrieving world state:', error);
      res.status(500).json({
        status: 'error',
        message: error.message,
      });
    }
  });

  /**
   * GET /api/sync/agents - Get agent status and information
   * Returns list of active agents and their status
   */
  router.get('/agents', (req, res) => {
    try {
      ensureMemoryDir();

      let agents = [];

      // Try to read from memory file
      if (fs.existsSync(AGENTS_FILE)) {
        const content = fs.readFileSync(AGENTS_FILE, 'utf8');
        const data = JSON.parse(content);
        agents = data.agents || [];
      }

      debug(`Retrieved ${agents.length} agents`);
      res.json({
        status: 'success',
        agents: agents,
        count: agents.length,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      debug('Error retrieving agents:', error);
      res.status(500).json({
        status: 'error',
        message: error.message,
      });
    }
  });

  /**
   * POST /api/sync/agents - Update agent status
   * Receives agent status updates from orchestrator
   */
  router.post('/agents', (req, res) => {
    try {
      ensureMemoryDir();

      const agents = req.body;

      // Validate agents array
      if (!Array.isArray(agents)) {
        return res.status(400).json({
          status: 'error',
          message: 'Expected array of agents',
        });
      }

      // Write to memory file
      fs.writeFileSync(
        AGENTS_FILE,
        JSON.stringify(
          {
            agents: agents,
            timestamp: new Date().toISOString(),
            count: agents.length,
          },
          null,
          2
        )
      );

      debug(`Updated ${agents.length} agents`);
      res.json({
        status: 'success',
        message: `Updated ${agents.length} agents`,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      debug('Error updating agents:', error);
      res.status(500).json({
        status: 'error',
        message: error.message,
      });
    }
  });

  /**
   * POST /api/sync/task-complete - Mark a task as completed
   * Receives completion notifications from orchestrator
   */
  router.post('/task-complete', (req, res) => {
    try {
      const { taskId, result } = req.body;

      if (!taskId) {
        return res.status(400).json({
          status: 'error',
          message: 'taskId is required',
        });
      }

      // Update database if available
      if (db && db.completeTask) {
        db.completeTask(taskId, result);
      }

      debug(`Task ${taskId} marked as completed`);
      res.json({
        status: 'success',
        message: `Task ${taskId} completed`,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      debug('Error marking task complete:', error);
      res.status(500).json({
        status: 'error',
        message: error.message,
      });
    }
  });

  /**
   * GET /api/sync/status - Get overall synchronization status
   * Returns status of all synchronized components
   */
  router.get('/status', (req, res) => {
    try {
      ensureMemoryDir();

      const status = {
        world_state: fs.existsSync(WORLD_STATE_FILE),
        tasks_queue: fs.existsSync(TASKS_QUEUE_FILE),
        agents: fs.existsSync(AGENTS_FILE),
        memory_dir: fs.existsSync(MEMORY_DIR),
      };

      res.json({
        status: 'success',
        sync_status: status,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      debug('Error getting sync status:', error);
      res.status(500).json({
        status: 'error',
        message: error.message,
      });
    }
  });

  return router;
}

module.exports = initOrchestrationBridge;
