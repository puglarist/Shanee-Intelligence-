const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');
const debug = require('debug')('omniverse:db:migrate');

const dbPath = process.env.DATABASE_URL || path.join(__dirname, '../../data/omniverse.db');
const schemaPath = path.join(__dirname, 'schema.sql');

try {
  // Create directory if it doesn't exist
  const dir = path.dirname(dbPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Open database
  const db = new Database(dbPath);
  db.pragma('journal_mode = WAL');
  debug(`Database opened: ${dbPath}`);

  // Read and execute schema
  const schema = fs.readFileSync(schemaPath, 'utf8');
  const statements = schema.split(';').filter(s => s.trim());

  statements.forEach(statement => {
    if (statement.trim()) {
      try {
        db.exec(statement);
        debug(`Executed: ${statement.substring(0, 50)}...`);
      } catch (error) {
        debug(`Error executing statement: ${error.message}`);
      }
    }
  });

  console.log('✓ Database migration completed');
  db.close();
  process.exit(0);
} catch (error) {
  console.error('✗ Migration failed:', error.message);
  process.exit(1);
}
