const express = require('express');
const debug = require('debug')('omniverse:api:sim');

module.exports = (db) => {
  const router = express.Router();

  // Simulation state
  let simState = {
    running: false,
    mode: 'earth', // 'earth', 'space'
    timeScale: 1.0,
    fps: 60,
    terrainQuality: 'medium',
    physicsEnabled: true
  };

  // Get simulation status
  router.get('/status', (req, res) => {
    try {
      res.json({
        status: 'ok',
        simulation: simState,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      debug('Error getting simulation status:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Start simulation
  router.post('/start', (req, res) => {
    try {
      const { mode = 'earth', timeScale = 1.0 } = req.body;

      simState.running = true;
      simState.mode = mode;
      simState.timeScale = timeScale;

      db.recordSync('simulation', 0, 'start');
      db.queueOfflineCommand('simulation.start', { mode, timeScale });

      res.status(200).json({
        status: 'ok',
        message: `Simulation started in ${mode} mode`,
        simulation: simState
      });
    } catch (error) {
      debug('Error starting simulation:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Stop simulation
  router.post('/stop', (req, res) => {
    try {
      simState.running = false;

      db.recordSync('simulation', 0, 'stop');
      db.queueOfflineCommand('simulation.stop', {});

      res.status(200).json({
        status: 'ok',
        message: 'Simulation stopped',
        simulation: simState
      });
    } catch (error) {
      debug('Error stopping simulation:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Set simulation parameters
  router.post('/config', (req, res) => {
    try {
      const { timeScale, terrainQuality, physicsEnabled } = req.body;

      if (timeScale !== undefined) simState.timeScale = timeScale;
      if (terrainQuality !== undefined) simState.terrainQuality = terrainQuality;
      if (physicsEnabled !== undefined) simState.physicsEnabled = physicsEnabled;

      db.recordSync('simulation', 0, 'config');
      db.queueOfflineCommand('simulation.config', { timeScale, terrainQuality, physicsEnabled });

      res.status(200).json({
        status: 'ok',
        message: 'Simulation configuration updated',
        simulation: simState
      });
    } catch (error) {
      debug('Error updating simulation config:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Get simulation metrics
  router.get('/metrics', (req, res) => {
    try {
      res.json({
        status: 'ok',
        metrics: {
          fps: simState.fps,
          mode: simState.mode,
          running: simState.running,
          timeScale: simState.timeScale,
          uptime: process.uptime(),
          memory: process.memoryUsage()
        }
      });
    } catch (error) {
      debug('Error getting simulation metrics:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  return router;
};
