const express = require('express');
const expressWs = require('express-ws');
const cors = require('cors');
const bodyParser = require('body-parser');
const debug = require('debug')('omniverse:server');
const path = require('path');
const fs = require('fs');

const config = require('./config/defaults');
const Database = require('./db/models');

// Initialize express app
const app = express();
expressWs(app);

// Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

// Initialize database
const db = new Database(config.database.path);

// Health check endpoint (local)
app.get('/health', (req, res) => {
  try {
    const status = db.getHealth();
    res.status(status.ok ? 200 : 503).json(status);
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
});

// API Routes
app.use('/api/world', require('./api/world')(db));
app.use('/api/assets', require('./api/assets')(db));
app.use('/api/sim', require('./api/sim')(db));
app.use('/api/sync', require('./api/sync')(db));

// WebSocket endpoint for real-time updates
app.ws('/ws/updates', (ws, req) => {
  debug('WebSocket client connected');

  ws.on('message', (msg) => {
    try {
      const data = JSON.parse(msg);
      debug('WebSocket message received:', data);

      // Handle different message types
      switch (data.type) {
        case 'subscribe':
          ws.clientId = data.clientId;
          ws.subscriptions = data.subscriptions || [];
          ws.send(JSON.stringify({ type: 'subscribed', status: 'ok' }));
          break;

        case 'command':
          // Queue command for offline execution
          db.queueOfflineCommand(data.command, data.payload);
          ws.send(JSON.stringify({ type: 'command_queued', id: data.id }));
          break;

        default:
          ws.send(JSON.stringify({ type: 'error', message: 'Unknown message type' }));
      }
    } catch (error) {
      debug('WebSocket error:', error);
      ws.send(JSON.stringify({ type: 'error', message: error.message }));
    }
  });

  ws.on('close', () => {
    debug('WebSocket client disconnected');
  });

  ws.on('error', (error) => {
    debug('WebSocket error:', error);
  });
});

// Error handling middleware
app.use((error, req, res, next) => {
  debug('Error:', error);
  res.status(error.status || 500).json({
    status: 'error',
    message: error.message,
    ...(config.nodeEnv === 'development' && { stack: error.stack })
  });
});

// Start server
const PORT = config.port;
app.listen(PORT, () => {
  debug(`Omniverse Engine Backend started on port ${PORT}`);
  debug(`Environment: ${config.nodeEnv}`);
  debug(`Database: ${config.database.path}`);
  debug(`External drive: ${config.externalDrive.basePath}`);
  console.log(`\nOmniverse Engine Backend`);
  console.log(`Running on http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  debug('SIGTERM received, shutting down gracefully');
  db.close();
  process.exit(0);
});

process.on('SIGINT', () => {
  debug('SIGINT received, shutting down gracefully');
  db.close();
  process.exit(0);
});

module.exports = app;
