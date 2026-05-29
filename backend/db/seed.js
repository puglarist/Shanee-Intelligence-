const Database = require('better-sqlite3');
const path = require('path');
const debug = require('debug')('omniverse:db:seed');

const dbPath = process.env.DATABASE_URL || path.join(__dirname, '../../data/omniverse.db');

try {
  const db = new Database(dbPath);
  debug(`Database opened: ${dbPath}`);

  // Seed initial world state
  db.prepare(`
    INSERT OR IGNORE INTO world_state (name, data, version)
    VALUES (?, ?, ?)
  `).run('default', JSON.stringify({
    name: 'Default World',
    description: 'Default Omniverse world',
    earthEnabled: true,
    spaceEnabled: true,
    physicsEnabled: true,
    terrainResolution: 256,
    time: 0,
    paused: false
  }), 1);

  debug('Seeded default world state');

  // Seed Bluetooth device table (empty by default)
  debug('Bluetooth devices table initialized');

  console.log('✓ Database seeding completed');
  db.close();
  process.exit(0);
} catch (error) {
  console.error('✗ Seeding failed:', error.message);
  process.exit(1);
}
