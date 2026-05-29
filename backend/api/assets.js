const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const debug = require('debug')('omniverse:api:assets');

module.exports = (db) => {
  const router = express.Router();

  // Calculate file hash
  function calculateHash(filePath) {
    const content = fs.readFileSync(filePath);
    return crypto.createHash('sha256').update(content).digest('hex');
  }

  // Register a new asset
  router.post('/register', (req, res) => {
    try {
      const { name, type, filePath, useExternalDrive } = req.body;

      if (!name || !type || !filePath) {
        return res.status(400).json({
          status: 'error',
          message: 'name, type, and filePath required'
        });
      }

      // Resolve path (local or external drive)
      let resolvedPath = filePath;
      let externalDrivePath = null;

      if (useExternalDrive) {
        resolvedPath = db.resolvePath(filePath);
        externalDrivePath = resolvedPath;
      }

      // Check if file exists
      if (!fs.existsSync(resolvedPath)) {
        return res.status(404).json({
          status: 'error',
          message: 'file not found'
        });
      }

      // Get file stats
      const stats = fs.statSync(resolvedPath);
      const hash = calculateHash(resolvedPath);

      // Register in database
      db.registerAsset(name, type, stats.size, hash, filePath, externalDrivePath);
      db.recordSync('asset', 0, 'register');

      res.status(201).json({
        status: 'ok',
        asset: {
          name,
          type,
          size: stats.size,
          hash,
          externalDrive: !!useExternalDrive
        }
      });
    } catch (error) {
      debug('Error registering asset:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Get asset metadata
  router.get('/:name', (req, res) => {
    try {
      const asset = db.getAsset(req.params.name);
      if (!asset) {
        return res.status(404).json({ status: 'not_found' });
      }

      res.json({
        status: 'ok',
        asset
      });
    } catch (error) {
      debug('Error fetching asset:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Stream asset file (chunked)
  router.get('/:name/stream', (req, res) => {
    try {
      const asset = db.getAsset(req.params.name);
      if (!asset) {
        return res.status(404).json({ status: 'not_found' });
      }

      const filePath = asset.external_drive_path || asset.path;

      if (!fs.existsSync(filePath)) {
        return res.status(404).json({ status: 'error', message: 'file not found' });
      }

      const stat = fs.statSync(filePath);
      const fileSize = stat.size;
      const chunkSize = 1024 * 1024; // 1MB chunks

      res.setHeader('Content-Type', 'application/octet-stream');
      res.setHeader('Content-Length', fileSize);
      res.setHeader('X-Asset-Name', asset.name);
      res.setHeader('X-Asset-Hash', asset.hash);

      const stream = fs.createReadStream(filePath, { highWaterMark: chunkSize });

      stream.on('error', (error) => {
        debug('Stream error:', error);
        if (!res.headersSent) {
          res.status(500).json({ status: 'error', message: error.message });
        }
      });

      stream.pipe(res);
    } catch (error) {
      debug('Error streaming asset:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  // Get assets by type
  router.get('/type/:type', (req, res) => {
    try {
      const assets = db.getAssetsByType(req.params.type);
      res.json({
        status: 'ok',
        type: req.params.type,
        count: assets.length,
        assets
      });
    } catch (error) {
      debug('Error fetching assets by type:', error);
      res.status(500).json({ status: 'error', message: error.message });
    }
  });

  return router;
};
