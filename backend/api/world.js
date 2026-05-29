const express = require('express');
const { v4: uuidv4 } = require('uuid');
const debug = require('debug')('omniverse:api:world');

module.exports = (db) => {
  const router = express.Router();

  // Get all world states
  router.get('/', (req, res) => {
    try {
      const states = db.getAllWorldStates();
      res.json({
        status: 'ok',
        count: states.length,
        states
      });
    } catch (error) {
      debug('Error fetching world states:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Get specific world state
  router.get('/:name', (req, res) => {
    try {
      const state = db.getWorldState(req.params.name);
      if (!state) {
        return res.status(404).json({ status: 'not_found' });
      }
      res.json({ status: 'ok', state });
    } catch (error) {
      debug('Error fetching world state:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Create or update world state
  router.post('/:name', (req, res) => {
    try {
      const { name } = req.params;
      const { data } = req.body;

      if (!data) {
        return res.status(400).json({ status: 'error', message: 'data field required' });
      }

      db.setWorldState(name, data);
      db.recordSync('world_state', 0, 'update');

      res.status(201).json({
        status: 'ok',
        message: `World state '${name}' saved`,
        name,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      debug('Error saving world state:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Get world statistics
  router.get('/stats/overview', (req, res) => {
    try {
      const stats = db.getStats();
      res.json({
        status: 'ok',
        stats
      });
    } catch (error) {
      debug('Error fetching statistics:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  return router;
};
