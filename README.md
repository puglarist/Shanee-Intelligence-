# Portable Omniverse Engine

A production-grade, fully portable simulation engine supporting GitHub Codespaces, external drive deployment, iOS Bluetooth remote control, and foundational Earth/space simulations.

## Features

- **GitHub Codespaces Support** - Native DevContainer configuration for seamless cloud development
- **External Drive Portability** - Run from USB drives or external SSDs with automatic path remapping
- **iOS Bluetooth Remote Control** - Native Swift app for device discovery and engine control
- **Offline-First Operation** - Work offline with automatic sync when reconnected
- **Earth Simulation** - Procedural terrain, weather systems, and day/night cycles
- **Space Simulation** - Orbital mechanics with realistic celestial body physics
- **Physics Engine** - Rigid body dynamics with collision detection
- **Asset Streaming** - Efficient loading of large assets with caching

## Quick Start

### Using GitHub Codespaces

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait for container to build (first time ~5 minutes)
3. Terminal opens automatically in `/workspace`

```bash
cd backend && npm run dev
```

### Local Development with Docker

```bash
# Build and start services
docker-compose up

# In another terminal
npm run bootstrap
cd backend && npm run dev
```

### Direct Installation

```bash
# Install dependencies
cd backend
npm ci

# Initialize database
npm run db:migrate

# Start server
npm run dev
```

## Project Structure

```
.
├── .devcontainer/           # GitHub Codespaces configuration
│   ├── devcontainer.json    # Container specification
│   ├── Dockerfile           # Multi-stage Docker build
│   └── docker-compose.yml   # Services orchestration
├── backend/                 # Node.js backend server
│   ├── api/                 # REST API endpoints
│   ├── sim/                 # Simulation engines
│   │   ├── earth.js         # Earth simulation
│   │   ├── space.js         # Space/orbital mechanics
│   │   └── physics.js       # Physics engine
│   ├── core/                # Core modules
│   │   ├── portable_runtime.js  # External drive support
│   │   └── asset_manager.js     # Asset handling
│   ├── db/                  # Database layer
│   │   ├── models.js        # Data models
│   │   ├── schema.sql       # Database schema
│   │   ├── migrate.js       # Migration script
│   │   └── seed.js          # Initial data
│   ├── config/              # Configuration
│   ├── storage/             # Storage modules
│   └── server.js            # Express server entry
├── ios/                     # iOS app (Swift)
│   ├── OmniverseRemote.swift    # Main app
│   └── BluetoothManager.swift   # BLE implementation
├── scripts/                 # Utility scripts
│   ├── bootstrap.sh         # Setup script
│   └── health-check.js      # Health endpoint
├── docs/                    # Documentation
└── docker-compose.yml       # Local development compose
```

## API Endpoints

### Health & Status
- `GET /health` - Server health check
- `GET /api/world/states` - List world states
- `GET /api/world/:name` - Get world state

### Simulation Control
- `POST /api/sim/start` - Start simulation
- `POST /api/sim/pause` - Pause simulation
- `POST /api/sim/reset` - Reset simulation
- `GET /api/sim/state` - Get current state

### Assets
- `GET /api/assets/list` - List available assets
- `GET /api/assets/:name` - Stream asset
- `POST /api/assets/register` - Register asset

### Synchronization
- `GET /api/sync/status` - Sync status
- `POST /api/sync/push` - Sync to cloud
- `POST /api/sync/pull` - Sync from cloud

### Bluetooth
- `GET /api/bluetooth/devices` - List paired devices
- `POST /api/bluetooth/command` - Send command

## WebSocket Events

Connect to `ws://localhost:3000/ws/updates` for real-time updates:

```javascript
{
  type: "subscribe",
  clientId: "client-123",
  subscriptions: ["world", "simulation", "assets"]
}
```

## iOS App Setup

### Requirements
- Xcode 15+
- iOS 14+
- Physical device or simulator with Bluetooth support

### Build & Run
```bash
cd ios
open OmniverseRemote.swift
# Build in Xcode: Cmd+B
# Run on device/simulator: Cmd+R
```

### Features
- Device discovery and pairing
- Real-time simulation control
- Offline command queue
- RSSI signal strength display

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL` - SQLite database path
- `EXTERNAL_DRIVE_PATH` - External storage mount point
- `PORT` - API server port (default: 3000)
- `DEBUG` - Debug namespaces (default: omniverse:*)

## External Drive Support

The engine automatically detects and uses external drives:

1. **Linux**: Scans `/proc/mounts` for `/media` and `/mnt` points
2. **macOS**: Checks `/Volumes` for mounted drives
3. **Windows**: Scans drive letters C-Z

Assets and data are stored hierarchically:
```
/media/external/omniverse/
├── earth/
├── space/
├── terrain/
└── cache/
```

Falls back to local `./data` if external drive unavailable.

## Offline Operation

Queued commands sync automatically when connection restored:

```javascript
// This queues if offline
POST /api/sim/pause
{
  queued: true,
  expiresIn: 2592000 // 30 days
}
```

## Database

SQLite database with WAL mode for portability:

- `world_state` - Simulation state snapshots
- `assets` - Asset metadata and paths
- `offline_queue` - Pending commands
- `sync_history` - Cloud sync history
- `simulation_state` - Entity states
- `bluetooth_devices` - Paired Bluetooth devices
- `bluetooth_commands` - Device command history

## Testing

```bash
# Run unit tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test suite
npm test -- api

# Watch mode
npm test -- --watch
```

## Logging

Debug logging enabled via `DEBUG` environment variable:

```bash
# All omniverse logs
DEBUG=omniverse:* npm run dev

# Specific modules
DEBUG=omniverse:sim:* npm run dev
DEBUG=omniverse:portable npm run dev
```

## Performance

Benchmarks on GitHub Codespaces:
- Server startup: ~2s
- Database ready: ~1s
- First API request: <100ms
- Terrain generation (256x256): ~500ms
- Orbital update (100 bodies): ~50ms

## Troubleshooting

### DevContainer not building
```bash
# Rebuild from scratch
docker-compose build --no-cache

# Check logs
docker-compose logs backend
```

### Database locked
```bash
# Reset database
rm -rf data/
npm run db:migrate && npm run db:seed
```

### Bluetooth connection fails
- Ensure iOS app has Bluetooth permission
- Check `DEBUG=omniverse:*` logs
- Verify pairing in device settings

### External drive not detected
```bash
# Check mount points
mount | grep -i omniverse

# Manually specify path
EXTERNAL_DRIVE_PATH=/mnt/usb npm run dev
```

## Contributing

1. Follow Node.js best practices
2. Use `npm run lint` to check code
3. Write tests for new features
4. Update documentation

## License

MIT

## Support

For issues and questions:
- GitHub Issues: [Create issue](https://github.com/puglarist/Shanee-Intelligence-/issues)
- Documentation: See `docs/` directory

## Roadmap

- [ ] Advanced terrain generation
- [ ] Multiplayer support
- [ ] Cloud synchronization (Firebase)
- [ ] AR visualization (iOS)
- [ ] Web dashboard
- [ ] Animation system
- [ ] Advanced physics (soft bodies)
- [ ] Procedural generation improvements
