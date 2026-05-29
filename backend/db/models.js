const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');
const debug = require('debug')('omniverse:db');

class OmniverseDatabase {
  constructor(dbPath) {
    this.dbPath = dbPath;
    this.db = null;
    this.init();
  }

  init() {
    // Create directory if it doesn't exist
    const dir = path.dirname(this.dbPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // Open database
    this.db = new Database(this.dbPath);
    this.db.pragma('journal_mode = WAL');
    this.db.pragma('synchronous = NORMAL');

    debug(`Database initialized at ${this.dbPath}`);
  }

  getHealth() {
    try {
      const result = this.db.prepare('SELECT 1').get();
      return {
        status: 'ok',
        ok: true,
        timestamp: new Date().toISOString(),
        database: this.dbPath
      };
    } catch (error) {
      debug('Health check failed:', error);
      return {
        status: 'error',
        ok: false,
        message: error.message
      };
    }
  }

  // World State Management
  getWorldState(name) {
    try {
      const stmt = this.db.prepare('SELECT data FROM world_state WHERE name = ?');
      const result = stmt.get(name);
      return result ? JSON.parse(result.data) : null;
    } catch (error) {
      debug('Error getting world state:', error);
      throw error;
    }
  }

  setWorldState(name, data) {
    try {
      const stmt = this.db.prepare(`
        INSERT OR REPLACE INTO world_state (name, data, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
      `);
      stmt.run(name, JSON.stringify(data));
      debug(`World state updated: ${name}`);
    } catch (error) {
      debug('Error setting world state:', error);
      throw error;
    }
  }

  getAllWorldStates() {
    try {
      const stmt = this.db.prepare(`
        SELECT name, data, created_at, updated_at FROM world_state
        ORDER BY updated_at DESC
      `);
      const results = stmt.all();
      return results.map(r => ({
        ...r,
        data: JSON.parse(r.data)
      }));
    } catch (error) {
      debug('Error getting all world states:', error);
      throw error;
    }
  }

  // Asset Management
  registerAsset(name, type, size, hash, assetPath, externalDrivePath = null) {
    try {
      const stmt = this.db.prepare(`
        INSERT OR REPLACE INTO assets (name, type, size, hash, path, external_drive_path)
        VALUES (?, ?, ?, ?, ?, ?)
      `);
      const result = stmt.run(name, type, size, hash, assetPath, externalDrivePath);
      debug(`Asset registered: ${name} (${type})`);
      return result.lastInsertRowid;
    } catch (error) {
      debug('Error registering asset:', error);
      throw error;
    }
  }

  getAsset(name) {
    try {
      const stmt = this.db.prepare('SELECT * FROM assets WHERE name = ?');
      return stmt.get(name);
    } catch (error) {
      debug('Error getting asset:', error);
      throw error;
    }
  }

  getAssetsByType(type) {
    try {
      const stmt = this.db.prepare('SELECT * FROM assets WHERE type = ? ORDER BY created_at DESC');
      return stmt.all(type);
    } catch (error) {
      debug('Error getting assets by type:', error);
      throw error;
    }
  }

  // Offline Queue Management
  queueOfflineCommand(command, payload = null) {
    try {
      const stmt = this.db.prepare(`
        INSERT INTO offline_queue (command, payload)
        VALUES (?, ?)
      `);
      const result = stmt.run(command, payload ? JSON.stringify(payload) : null);
      debug(`Command queued: ${command}`);
      return result.lastInsertRowid;
    } catch (error) {
      debug('Error queueing offline command:', error);
      throw error;
    }
  }

  getOfflineQueue() {
    try {
      const stmt = this.db.prepare(`
        SELECT id, command, payload FROM offline_queue
        WHERE synced = 0
        ORDER BY created_at ASC
        LIMIT 1000
      `);
      const results = stmt.all();
      return results.map(r => ({
        ...r,
        payload: r.payload ? JSON.parse(r.payload) : null
      }));
    } catch (error) {
      debug('Error getting offline queue:', error);
      throw error;
    }
  }

  markQueueItemSynced(id) {
    try {
      const stmt = this.db.prepare(`
        UPDATE offline_queue SET synced = 1 WHERE id = ?
      `);
      stmt.run(id);
      debug(`Queue item marked as synced: ${id}`);
    } catch (error) {
      debug('Error marking queue item as synced:', error);
      throw error;
    }
  }

  clearOldQueueItems(days = 30) {
    try {
      const stmt = this.db.prepare(`
        DELETE FROM offline_queue
        WHERE synced = 1 AND created_at < datetime('now', '-' || ? || ' days')
      `);
      const result = stmt.run(days);
      debug(`Cleared ${result.changes} old queue items`);
    } catch (error) {
      debug('Error clearing old queue items:', error);
      throw error;
    }
  }

  // Sync History
  recordSync(entityType, entityId, action) {
    try {
      const stmt = this.db.prepare(`
        INSERT INTO sync_history (entity_type, entity_id, action, synced)
        VALUES (?, ?, ?, 1)
      `);
      stmt.run(entityType, entityId, action);
      debug(`Sync recorded: ${entityType} #${entityId} - ${action}`);
    } catch (error) {
      debug('Error recording sync:', error);
      throw error;
    }
  }

  getPendingSyncs() {
    try {
      const stmt = this.db.prepare(`
        SELECT * FROM sync_history WHERE synced = 0 ORDER BY timestamp ASC
      `);
      return stmt.all();
    } catch (error) {
      debug('Error getting pending syncs:', error);
      throw error;
    }
  }

  // Portable Storage Path Remapping
  resolvePath(logicalPath) {
    const config = require('../config/defaults');
    const basePath = config.externalDrive.basePath;

    // Check if external drive is accessible
    if (fs.existsSync(basePath)) {
      return path.join(basePath, logicalPath);
    }

    // Fallback to local workspace
    return path.join(process.cwd(), '..', 'data', logicalPath);
  }

  // Database Maintenance
  optimize() {
    try {
      this.db.exec('VACUUM');
      debug('Database optimized');
    } catch (error) {
      debug('Error optimizing database:', error);
    }
  }

  close() {
    if (this.db) {
      this.db.close();
      debug('Database connection closed');
    }
  }

  // Statistics
  getStats() {
    try {
      const worldStates = this.db.prepare('SELECT COUNT(*) as count FROM world_state').get();
      const assets = this.db.prepare('SELECT COUNT(*) as count FROM assets').get();
      const queuedCommands = this.db.prepare('SELECT COUNT(*) as count FROM offline_queue WHERE synced = 0').get();

      return {
        worldStates: worldStates.count,
        assets: assets.count,
        queuedCommands: queuedCommands.count,
        databaseSize: fs.statSync(this.dbPath).size,
        lastOptimized: new Date().toISOString()
      };
    } catch (error) {
      debug('Error getting statistics:', error);
      throw error;
    }
  }
}

module.exports = OmniverseDatabase;
