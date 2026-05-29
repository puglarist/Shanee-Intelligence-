-- Omniverse Engine Database Schema
-- Version: 1.0.0

-- World State Table
CREATE TABLE IF NOT EXISTS world_state (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  data TEXT NOT NULL,
  version INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_synced_at TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_updated_at (updated_at)
);

-- Assets Table
CREATE TABLE IF NOT EXISTS assets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  type TEXT NOT NULL,
  size INTEGER,
  hash TEXT,
  path TEXT NOT NULL,
  external_drive_path TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  cached BOOLEAN DEFAULT 0,
  cached_at TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_type (type)
);

-- Offline Command Queue
CREATE TABLE IF NOT EXISTS offline_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  command TEXT NOT NULL,
  payload TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  processed_at TIMESTAMP,
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,
  expires_at TIMESTAMP,
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);

-- Sync History Table
CREATE TABLE IF NOT EXISTS sync_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  action TEXT NOT NULL,
  local_version INTEGER,
  remote_version INTEGER,
  conflict BOOLEAN DEFAULT 0,
  resolved_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_entity (entity_type, entity_id),
  INDEX idx_created_at (created_at)
);

-- Simulation Data Table
CREATE TABLE IF NOT EXISTS simulation_state (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  data TEXT NOT NULL,
  position_x REAL,
  position_y REAL,
  position_z REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(entity_type, entity_id),
  INDEX idx_entity (entity_type),
  INDEX idx_position (position_x, position_y, position_z)
);

-- Bluetooth Devices Table
CREATE TABLE IF NOT EXISTS bluetooth_devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_uuid TEXT UNIQUE NOT NULL,
  device_name TEXT NOT NULL,
  mac_address TEXT,
  paired BOOLEAN DEFAULT 0,
  last_seen TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_uuid (device_uuid),
  INDEX idx_paired (paired)
);

-- Bluetooth Commands Table
CREATE TABLE IF NOT EXISTS bluetooth_commands (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_uuid TEXT NOT NULL,
  command TEXT NOT NULL,
  payload TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  executed_at TIMESTAMP,
  error_message TEXT,
  FOREIGN KEY (device_uuid) REFERENCES bluetooth_devices(device_uuid),
  INDEX idx_device (device_uuid),
  INDEX idx_status (status)
);

-- Create triggers for updated_at
CREATE TRIGGER IF NOT EXISTS world_state_update
AFTER UPDATE ON world_state
FOR EACH ROW
BEGIN
  UPDATE world_state SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS assets_update
AFTER UPDATE ON assets
FOR EACH ROW
BEGIN
  UPDATE assets SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS simulation_state_update
AFTER UPDATE ON simulation_state
FOR EACH ROW
BEGIN
  UPDATE simulation_state SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS bluetooth_devices_update
AFTER UPDATE ON bluetooth_devices
FOR EACH ROW
BEGIN
  UPDATE bluetooth_devices SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
