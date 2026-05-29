const path = require('path');
const os = require('os');

module.exports = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 3000,
  healthCheckPort: process.env.HEALTH_CHECK_PORT || 8080,

  // Database configuration
  database: {
    path: process.env.DATABASE_URL || path.join(__dirname, '../../data/omniverse.db'),
    enableWAL: true,
    synchronous: 'NORMAL'
  },

  // External drive configuration
  externalDrive: {
    basePath: process.env.EXTERNAL_DRIVE_PATH || '/media/external',
    fallbackPath: path.join(__dirname, '../../data'),
    enabled: process.env.EXTERNAL_DRIVE_ENABLED !== 'false',
    detectTimeout: 5000
  },

  // Asset configuration
  assets: {
    maxFileSize: 1024 * 1024 * 1024, // 1GB
    chunkSize: 1024 * 1024 * 5, // 5MB chunks
    cacheTTL: 3600 * 24 * 7, // 7 days
    cacheDir: path.join(__dirname, '../../data/cache')
  },

  // Offline configuration
  offline: {
    queueMaxSize: 1000,
    queueExpiration: 3600 * 24 * 30, // 30 days
    syncInterval: 30000 // 30 seconds
  },

  // Simulation configuration
  simulation: {
    earthTexturePath: '/assets/earth',
    skyboxPath: '/assets/skybox',
    terrainResolution: 256,
    physicsFPS: 60
  },

  // Bluetooth configuration (iOS integration)
  bluetooth: {
    deviceName: 'Omniverse-' + os.hostname().slice(0, 4),
    serviceUUID: 'OmniverseService',
    commandCharacteristic: 'OmniverseCommand',
    stateCharacteristic: 'OmniverseState',
    discoveryTimeout: 30000,
    reconnectInterval: 5000,
    maxReconnectAttempts: 10
  },

  // Logging configuration
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    format: 'json',
    colorize: process.env.NODE_ENV !== 'production'
  }
};
