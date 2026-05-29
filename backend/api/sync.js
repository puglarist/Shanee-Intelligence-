const express = require('express');
const debug = require('debug')('omniverse:api:sync');

module.exports = (db) => {
  const router = express.Router();

  // Get offline queue
  router.get('/queue', (req, res) => {
    try {
      const queue = db.getOfflineQueue();
      res.json({
        status: 'ok',
        queueLength: queue.length,
        queue
      });
    } catch (error) {
      debug('Error fetching offline queue:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Process offline queue (from cloud or other source)
  router.post('/process-queue', (req, res) => {
    try {
      const queue = db.getOfflineQueue();

      // Simulate processing each command
      const results = queue.map(item => {
        try {
          // In production, execute the command
          db.markQueueItemSynced(item.id);
          return { id: item.id, status: 'processed' };
        } catch (error) {
          return { id: item.id, status: 'error', message: error.message };
        }
      });

      // Clean up old items
      db.clearOldQueueItems(30);

      res.json({
        status: 'ok',
        message: `Processed ${results.filter(r => r.status === 'processed').length} queued commands`,
        results
      });
    } catch (error) {
      debug('Error processing offline queue:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Sync with cloud (optional)
  router.post('/cloud-sync', (req, res) => {
    try {
      const { entityType, entityId, direction = 'both' } = req.body;

      // Log sync attempt
      db.recordSync(entityType, entityId, 'cloud_sync');

      res.json({
        status: 'ok',
        message: 'Cloud sync initiated',
        entityType,
        entityId,
        direction,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      debug('Error initiating cloud sync:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Get sync history
  router.get('/history', (req, res) => {
    try {
      const limit = req.query.limit || 100;
      const syncs = db.getPendingSyncs().slice(0, limit);

      res.json({
        status: 'ok',
        count: syncs.length,
        syncs
      });
    } catch (error) {
      debug('Error fetching sync history:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  return router;
};
