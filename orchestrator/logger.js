import fs from 'fs';
import path from 'path';

const LOG_DIR = './logs';
const LOG_FILE = path.join(LOG_DIR, 'execution.log');

// Ensure logs directory exists
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

export class Logger {
  constructor(module = 'system') {
    this.module = module;
  }

  log(level, message) {
    const timestamp = new Date().toISOString();
    const prefix = `[${timestamp}] [${level}] [${this.module}]`;
    const logEntry = `${prefix} ${message}`;

    console.log(logEntry);

    try {
      fs.appendFileSync(LOG_FILE, logEntry + '\n');
    } catch (error) {
      console.error(`Failed to write to log file: ${error.message}`);
    }
  }

  info(message) {
    this.log('INFO', message);
  }

  error(message) {
    this.log('ERROR', message);
  }

  warn(message) {
    this.log('WARN', message);
  }

  debug(message) {
    if (process.env.DEBUG) {
      this.log('DEBUG', message);
    }
  }
}
