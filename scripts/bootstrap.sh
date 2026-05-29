#!/bin/bash

set -e

echo "======================================"
echo "Omniverse Engine - Bootstrap Script"
echo "======================================"

# Create necessary directories
echo "[1/6] Creating directories..."
mkdir -p /workspace/data
mkdir -p /workspace/logs
mkdir -p /media/external

# Install backend dependencies
echo "[2/6] Installing Node.js dependencies..."
cd /workspace/backend
npm install

# Initialize database
echo "[3/6] Initializing database..."
node << 'EOF'
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const dbPath = '/workspace/data/omniverse.db';
const db = new Database(dbPath);

// Enable WAL mode for better concurrency
db.pragma('journal_mode = WAL');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS world_state (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    data JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,
    size INTEGER,
    hash TEXT,
    path TEXT,
    external_drive_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS sync_history (
    id INTEGER PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    synced BOOLEAN DEFAULT 0
  );

  CREATE TABLE IF NOT EXISTS offline_queue (
    id INTEGER PRIMARY KEY,
    command TEXT NOT NULL,
    payload JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    synced BOOLEAN DEFAULT 0
  );

  CREATE INDEX IF NOT EXISTS idx_world_state_name ON world_state(name);
  CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(type);
  CREATE INDEX IF NOT EXISTS idx_sync_history_synced ON sync_history(synced);
  CREATE INDEX IF NOT EXISTS idx_offline_queue_synced ON offline_queue(synced);
`);

console.log('Database initialized successfully at:', dbPath);
db.close();
EOF

# Create configuration files
echo "[4/6] Creating configuration files..."
cat > /workspace/backend/config/defaults.js << 'EOF'
module.exports = {
  port: process.env.PORT || 3000,
  healthCheckPort: process.env.HEALTH_CHECK_PORT || 8080,
  nodeEnv: process.env.NODE_ENV || 'development',
  database: {
    path: process.env.DATABASE_URL || '/workspace/data/omniverse.db'
  },
  externalDrive: {
    basePath: process.env.EXTERNAL_DRIVE_PATH || '/media/external',
    enabled: true
  },
  api: {
    corsEnabled: true,
    websocketEnabled: true
  },
  simulation: {
    terrainQuality: 'medium',
    physicsEnabled: true
  }
};
EOF

# Run health check script creation
echo "[5/6] Setting up health check..."
cat > /workspace/scripts/health-check.js << 'EOF'
const http = require('http');
const path = require('path');
const fs = require('fs');

const port = process.env.HEALTH_CHECK_PORT || 8080;

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    try {
      const dbPath = process.env.DATABASE_URL || '/workspace/data/omniverse.db';

      // Check if database exists
      if (!fs.existsSync(dbPath)) {
        res.writeHead(503, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'unavailable', reason: 'database_not_found' }));
        return;
      }

      // Check if external drive accessible
      const externalDrivePath = process.env.EXTERNAL_DRIVE_PATH || '/media/external';
      let externalDriveAccessible = false;

      try {
        fs.accessSync(externalDrivePath, fs.constants.F_OK);
        externalDriveAccessible = true;
      } catch (e) {
        // External drive not accessible, but not critical
      }

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        status: 'ok',
        timestamp: new Date().toISOString(),
        services: {
          database: 'ready',
          externalDrive: externalDriveAccessible ? 'ready' : 'unavailable'
        },
        uptime: process.uptime()
      }));
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'error', message: error.message }));
    }
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

server.listen(port, () => {
  console.log(`Health check service listening on port ${port}`);
});
EOF

# Install better-sqlite3
echo "[6/6] Finalizing setup..."
npm install better-sqlite3

echo ""
echo "======================================"
echo "Bootstrap Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Backend server: npm run dev (port 3000)"
echo "2. Health check: node scripts/health-check.js (port 8080)"
echo "3. Database: /workspace/data/omniverse.db"
echo ""
