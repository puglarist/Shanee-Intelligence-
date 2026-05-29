# Portable Omniverse Engine - Architecture

## System Overview

The Portable Omniverse Engine is a distributed simulation system designed for:
- **Portability**: Runs from external drives with zero installation
- **Offline Operation**: Works completely disconnected with sync on reconnection
- **Mobile Control**: iOS remote control via Bluetooth LE
- **Cross-Platform**: Linux, macOS, Windows, GitHub Codespaces
- **Extensibility**: Modular architecture for custom simulations

## Component Architecture

### 1. Backend Server (Node.js + Express)

```
Backend Server (port 3000)
├── Express.js Application
│   ├── REST API Layer
│   │   ├── World Management (/api/world/*)
│   │   ├── Asset Management (/api/assets/*)
│   │   ├── Simulation Control (/api/sim/*)
│   │   ├── Synchronization (/api/sync/*)
│   │   └── Bluetooth Interface (/api/bluetooth/*)
│   ├── WebSocket Layer (port 3000/ws)
│   │   ├── Real-time updates
│   │   ├── Command subscription
│   │   └── State synchronization
│   └── Middleware
│       ├── CORS handling
│       ├── Body parsing
│       ├── Error handling
│       └── Logging/debugging
├── Core Modules
│   ├── PortableRuntime
│   │   ├── Path resolution
│   │   ├── Mount detection
│   │   └── Asset discovery
│   └── AssetManager
│       ├── Asset registration
│       ├── Streaming
│       ├── Caching
│       └── Integrity checking
├── Simulation Engines
│   ├── EarthSimulation
│   │   ├── Terrain generation
│   │   ├── Weather system
│   │   └── Day/night cycle
│   ├── SpaceSimulation
│   │   ├── Orbital mechanics
│   │   ├── Celestial bodies
│   │   └── Time scale control
│   └── PhysicsEngine
│       ├── Rigid body dynamics
│       ├── Collision detection
│       └── Force/torque application
└── Data Layer
    ├── SQLite Database
    │   ├── World state
    │   ├── Assets
    │   ├── Offline queue
    │   ├── Sync history
    │   ├── Simulation entities
    │   └── Bluetooth devices
    └── Configuration
        ├── Environment variables
        ├── Default settings
        └── Local overrides
```

### 2. iOS Remote Control App (SwiftUI)

```
iOS App
├── SwiftUI Views
│   ├── ContentView (main navigation)
│   ├── DeviceDiscoveryView (Bluetooth scanning)
│   ├── ConnectedControlView (simulation controls)
│   ├── SettingsView (app preferences)
│   └── StateDisplayView (status information)
├── Bluetooth Manager
│   ├── CBCentralManager
│   │   ├── Device discovery
│   │   └── Peripheral connection
│   ├── CBPeripheral
│   │   ├── Service discovery
│   │   ├── Characteristic discovery
│   │   └── Data notification
│   └── GATT Communication
│       ├── Command characteristic (write)
│       ├── State characteristic (read/notify)
│       └── Command protocol
└── Local State
    ├── Command queue
    ├── Device pairing
    ├── App settings
    └── Offline state
```

### 3. Data Flow

#### Simulation Execution Flow

```
1. Client Request → WebSocket/HTTP
   ↓
2. Backend API Handler
   ├── Parse command
   ├── Validate state
   └── Queue if offline
   ↓
3. Simulation Engine Update
   ├── Apply forces/accelerations
   ├── Update positions/velocities
   ├── Detect collisions
   └── Integrate step
   ↓
4. Database Storage
   ├── Update world state
   ├── Record sync history
   └── Queue for cloud sync
   ↓
5. Client Notification
   ├── WebSocket broadcast
   ├── iOS push (if Bluetooth connected)
   └── Store in offline queue
```

#### Offline Synchronization Flow

```
1. Device Disconnected
   ├── Commands queued locally (iOS)
   └── Changes stored in database (Backend)
   
2. Device Reconnected
   ├── iOS detects connection
   ├── Backend reconnection handler
   └── Conflict detection
   
3. Conflict Resolution
   ├── Compare local + remote versions
   ├── Apply merge strategy
   │   ├── Last-write-wins
   │   ├── Custom resolver
   │   └── Manual review
   └── Sync complete
   
4. State Consistency
   ├── Update all affected entities
   ├── Broadcast to all clients
   └── Log sync history
```

## Module Specifications

### PortableRuntime

**Purpose**: Abstract storage layer for cross-platform portability

**Key Methods**:
- `resolvePath(name, type)` - Find asset on any storage
- `detectStoragePaths()` - Scan for external drives
- `assetExists(name, type)` - Check availability
- `listAssets(type)` - Enumerate assets
- `getStorageInfo()` - Mount point info

**Path Resolution Strategy**:
```
1. Check asset cache
2. Scan external drive (EXTERNAL_DRIVE_PATH)
3. Scan fallback path (./data)
4. Scan detected mounts (Linux/macOS/Windows)
5. Return fallback path
```

### AssetManager

**Purpose**: Unified asset loading and streaming

**Key Methods**:
- `registerAsset(name, type, path)` - Add to registry
- `streamAsset(name, res)` - Send chunks to client
- `cacheAsset(name)` - Copy to local cache
- `getAsset(name)` - Load into memory
- `discoverAssets(type)` - Find on disk

**Streaming**:
- Configurable chunk size (default 5MB)
- SHA-256 integrity hashing
- Progress reporting
- Resume support

### EarthSimulation

**Purpose**: Realistic Earth environment simulation

**State Variables**:
- `timeOfDay` (0-24 hours)
- `terrainHeightMap` (2D array)
- `atmosphericSettings` (wind, temperature, humidity)
- `dayNightCycleEnabled` (boolean)

**Update Cycle**:
```
1. Update time of day
2. Calculate sun position (altitude/azimuth)
3. Compute sky lighting
4. Update weather
5. Return state for rendering
```

### SpaceSimulation

**Purpose**: N-body orbital mechanics

**Key Entities**:
- Sun (stationary reference frame)
- Planets (Earth, Mars)
- Satellites (Moon)
- Custom spacecraft (user-defined)

**Physics**:
```
Force = G * m1 * m2 / r²
Acceleration = Force / mass
Velocity += Acceleration * dt
Position += Velocity * dt
```

**Time Scaling**:
- Real-time: 1x
- Fast-forward: 10000x+
- Pause: 0x

### PhysicsEngine

**Purpose**: Rigid body dynamics and collision

**Entities**:
- Position, velocity, acceleration
- Angular velocity, torque
- Mass, radius, shape
- Friction, restitution, damping

**Update Steps**:
1. Calculate forces from all bodies
2. Integrate velocities (v += a*dt)
3. Resolve collisions
4. Integrate positions (p += v*dt)
5. Apply damping

**Collision Response**:
- Sphere-sphere detection (distance < r1 + r2)
- Separation (push apart)
- Impulse resolution (conservation of momentum)
- Restitution (bounce factor)

## Data Model

### World State

```javascript
{
  name: "Default World",
  description: "...",
  earthEnabled: true,
  spaceEnabled: true,
  physicsEnabled: true,
  time: 1234.5,
  paused: false,
  version: 1,
  updated_at: "2026-05-29T12:00:00Z"
}
```

### Asset Metadata

```javascript
{
  name: "terrain_001",
  type: "earth",
  size: 52428800,
  hash: "sha256:...",
  path: "/media/external/omniverse/earth/terrain_001",
  cached: true,
  registered: "2026-05-29T12:00:00Z"
}
```

### Offline Queue Entry

```javascript
{
  command: "PAUSE",
  payload: { speed: 0 },
  status: "pending", // pending|processed|failed
  created_at: "2026-05-29T12:00:00Z",
  expires_at: "2026-06-28T12:00:00Z",
  retryCount: 0
}
```

### Bluetooth Command

```javascript
{
  device_uuid: "...",
  command: "CAMERA_EARTH",
  payload: "{ ... }",
  status: "pending", // pending|executed|failed
  created_at: "2026-05-29T12:00:00Z"
}
```

## Communication Protocols

### REST API

**Health Check**
```
GET /health
Response: { status: 'ok', ok: true, timestamp: '...', database: '...' }
```

**World Control**
```
GET /api/world/states
POST /api/world/reset
GET /api/world/default
```

**Simulation Control**
```
POST /api/sim/start { speed: 1 }
POST /api/sim/pause
POST /api/sim/reset
GET /api/sim/state
```

### WebSocket Events

**Subscribe**
```javascript
{
  type: "subscribe",
  clientId: "client-123",
  subscriptions: ["world", "simulation"]
}
Response: { type: "subscribed", status: "ok" }
```

**Command**
```javascript
{
  type: "command",
  command: "PAUSE",
  payload: {...},
  id: "cmd-456"
}
Response: { type: "command_queued", id: "cmd-456" }
```

### Bluetooth LE

**Service UUID**: `OmniverseService`

**Characteristics**:
- `OmniverseCommand` (write) - Send commands
- `OmniverseState` (read+notify) - Receive state updates

**Command Format** (JSON over BLE):
```json
{
  "command": "PLAY",
  "payload": { "timeScale": 1 },
  "id": "cmd-123"
}
```

**State Format** (JSON over BLE):
```json
{
  "type": "state_update",
  "world": {...},
  "simulation": {...},
  "timestamp": "..."
}
```

## Deployment Scenarios

### 1. GitHub Codespaces

```
Container (Node 20 + SQLite)
├── Mounted codebase
├── Volume: omniverse-data
└── Exposed ports: 3000, 3001, 8080
```

### 2. External Drive (USB 3.0)

```
/media/external/
├── omniverse/
│   ├── app/       (node_modules, executable)
│   ├── data/      (omniverse.db, configs)
│   ├── assets/    (terrain, space, etc.)
│   └── cache/     (streaming cache)
```

### 3. iOS Remote

```
iPhone/iPad (iOS 14+)
├── SwiftUI App
├── Core Bluetooth
├── Offline queue (local storage)
└── Network socket (TCP/Bluetooth)
```

## Performance Considerations

### Database
- WAL mode for concurrent access
- Indexes on frequently queried columns
- Connection pooling
- Query optimization via EXPLAIN PLAN

### Physics
- Spatial partitioning for collision (future)
- Frame rate lock at 60 FPS
- Adaptive time stepping
- GPU acceleration (future - Three.js)

### Assets
- Chunked streaming (5MB default)
- LRU caching with TTL
- Lazy loading
- Progressive loading indicator

### Networking
- WebSocket compression
- Delta updates (only changed fields)
- Batch commands in queues
- Connection pooling

## Security

### Data Integrity
- SHA-256 hashing of assets
- Database ACID compliance
- Transaction logging
- Corruption recovery

### Access Control (Future)
- User authentication
- Role-based permissions
- Audit logging
- Rate limiting

### Encryption (Future)
- TLS for network
- SQLite encryption
- iOS Keychain for secrets
- Bluetooth pairing validation

## Extensibility Points

### Custom Simulations
```javascript
class CustomSimulation {
  constructor(config) { }
  initialize() { }
  update(deltaTime) { }
  getState() { }
}

// Register: simManager.register('custom', CustomSimulation);
```

### Asset Loaders
```javascript
// Custom asset format support
assetManager.registerLoader('gltf', gltfLoader);
assetManager.registerLoader('terrain', terrainLoader);
```

### Bluetooth Commands
```javascript
// Custom command handlers
bluetoothManager.registerCommand('CUSTOM', customHandler);
```

## Future Roadmap

### Short Term
- Web-based dashboard
- Advanced terrain generation (erosion simulation)
- Animation system
- Multiplayer support (WebRTC)

### Medium Term
- Cloud synchronization (Firebase)
- AR visualization (iOS)
- Advanced physics (soft bodies, particles)
- Procedural universe generation

### Long Term
- Real-time multiplayer scaling
- Machine learning integration
- GPU-accelerated rendering
- Enterprise deployment

---

For implementation details, see specific module documentation in `docs/` directory.
