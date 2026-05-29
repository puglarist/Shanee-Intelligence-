# Omniverse Engine - System Architecture

Complete technical reference for the unified system architecture combining the Portable Backend with HF Swarm Orchestrator.

## System Overview

The Omniverse Engine is a multi-layered simulation platform:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Clients & Frontends                         │
│   iOS (Swift/Bluetooth) │ Web Dashboard │ External Tools             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                    Express.js REST API Layer                        │
│   /api/sim  │  /api/assets  │  /api/sync  │  /api/world             │
│              WebSocket: /ws/updates                                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
┌───────▼──────────────┐            ┌────────────▼──────────────┐
│  Simulation Engines  │            │  FastAPI Orchestrator     │
│  - Earth             │            │  (Python, Port 8000)      │
│  - Space             │            │                          │
│  - Physics           │            │  - Agent Management      │
│                      │            │  - Task Scheduling       │
│  Node.js             │            │  - Swarm Coordination    │
│  (Port 3000)         │            │  - State Tracking        │
└───────┬──────────────┘            └────────────┬──────────────┘
        │                                        │
        │           ┌───────────────────────────┘
        │           │
┌───────▼───────────▼──────────────────────────────┐
│         Persistent Data Layer (Prisma/SQLite)    │
│  - Agent State         - Task Queue              │
│  - Simulation State    - Execution Logs          │
│  - World State         - Checkpoints             │
│  - Metrics             - Sync History            │
└──────────────────────────┬───────────────────────┘
                           │
┌──────────────────────────▼───────────────────────┐
│         Storage Layer                            │
│  - SQLite Database     - External Drives         │
│  - Asset Cache         - Memory Files            │
│  - Offline Queues                               │
└────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Express.js Backend (`backend/`)

**Purpose**: REST API server and simulation management

**Key Files**:
- `server.js` - Express server setup and middleware
- `api/world.js` - World state management endpoints
- `api/sim.js` - Simulation control endpoints
- `api/assets.js` - Asset discovery and streaming
- `api/sync.js` - Offline queue and sync endpoints

**API Endpoints**:

```
GET /health                    # Server health check
GET /api/world/states         # List all worlds
GET /api/world/:name          # Get world state
POST /api/sim/start           # Start simulation
POST /api/sim/pause           # Pause simulation
POST /api/sim/reset           # Reset simulation
GET /api/sim/state            # Current simulation state
GET /api/assets/list          # List available assets
GET /api/assets/:name         # Stream asset
POST /api/assets/register     # Register asset
GET /api/sync/status          # Sync status
POST /api/sync/push           # Push to cloud
POST /api/sync/pull           # Pull from cloud
WS /ws/updates                # WebSocket for real-time updates
```

### 2. Simulation Engines (`backend/sim/`)

#### Earth Simulation (`earth.js`)

Procedural Earth environment generator:

```javascript
class EarthSim {
  constructor(options)
  generateTerrain()              // Perlin noise-based terrain
  getWeatherAt(lat, lon)         // Weather at location
  updateDayNightCycle(deltaTime) // Sun positioning
  getRenderData()                // Visualization data
}
```

**Features**:
- Noise-based terrain generation
- Weather system (wind, temperature, humidity, UV)
- Day/night cycle with atmospheric lighting
- Real-time environmental updates

#### Space Simulation (`space.js`)

Orbital mechanics engine:

```javascript
class SpaceSim {
  constructor()
  addCelestialBody(body)         // Sun, planets, moons
  update(deltaTime)              // N-body gravity calculations
  getOrbitalState()              // Current positions
  getState()                     // Full system state
}
```

**Features**:
- Solar system initialization
- N-body gravitational physics (F = G * m1 * m2 / r²)
- Realistic orbital parameters (AU, velocity, mass)
- Time scaling for fast-forward simulation

#### Physics Engine (`physics.js`)

Rigid body dynamics:

```javascript
class PhysicsEngine {
  addBody(body)                  // Add rigid body
  update(deltaTime)              // Physics iteration
  getCollisions()                // Collision detection
  applyForce(bodyId, force)      // Apply force
}
```

**Features**:
- Sphere-sphere collision detection
- Collision response with restitution
- Linear and angular damping
- Multi-step integration (Euler method)

### 3. Portable Runtime (`backend/core/`)

#### Portable Runtime (`portable_runtime.js`)

Cross-platform path resolution:

```javascript
class PortableRuntime {
  detectExternalDrives()         // Find mounted drives
  getAssetPath(assetName)        // Resolve asset paths
  getDataPath()                  // Get storage directory
  resolvePath(path)              // Normalize paths
}
```

**Platforms Supported**:
- Linux: `/proc/mounts`, `/media`, `/mnt`
- macOS: `/Volumes` scanning
- Windows: Drive letter enumeration (C-Z)

#### Asset Manager (`asset_manager.js`)

Asset discovery and streaming:

```javascript
class AssetManager {
  discoverAssets()               // Find assets on drives
  getAsset(name)                 // Retrieve asset
  streamAsset(name, callback)    // Stream in chunks
  cacheAsset(name)               // Cache to memory
  validateIntegrity(data)        // SHA-256 check
}
```

**Features**:
- Progressive asset discovery
- Chunked streaming (5MB default)
- SHA-256 integrity verification
- LRU caching with TTL

### 4. Database Layer (`backend/db/`)

#### Models (`models.js`)

SQLite database abstraction:

```javascript
class Database {
  getWorldState(name)            // Get world
  setWorldState(name, data)      // Save world
  getAssetMetadata(name)         // Asset info
  queueOfflineCommand(cmd, data) // Queue for sync
  getOfflineQueue()              // Pending commands
  deleteWorldState(name)         // Remove world
}
```

#### Schema (`schema.sql`)

7 core tables:

1. **world_state** - Simulation snapshots
   - `id`, `name`, `data`, `timestamp`, `version`

2. **assets** - Asset metadata
   - `id`, `name`, `path`, `hash`, `size`, `metadata`

3. **offline_queue** - Offline commands
   - `id`, `command`, `payload`, `status`, `created_at`, `expiresAt`

4. **sync_history** - Cloud sync records
   - `id`, `type`, `timestamp`, `status`, `details`

5. **simulation_state** - Entity states
   - `id`, `world_id`, `entity_id`, `data`, `timestamp`

6. **bluetooth_devices** - Paired devices
   - `id`, `uuid`, `name`, `rssi`, `paired_at`

7. **bluetooth_commands** - Command history
   - `id`, `device_id`, `command`, `result`, `timestamp`

### 5. FastAPI Orchestrator (`orchestrator/`)

**Purpose**: AI swarm coordination and task scheduling

**Key Files**:
- `main.py` - FastAPI REST API server
- `agents/__init__.py` - Agent registry and base classes
- `agents/coordinator.py` - Multi-agent coordination
- `agents/earth_sim.py` - Earth simulation agent
- `tasks/queue.py` - Task scheduling and management
- `config.py` - Configuration and environment setup
- `hf_client.py` - Hugging Face API integration

**API Endpoints**:

```
GET /health                    # Orchestrator health
GET /agents                    # List all agents
GET /agents/{name}             # Agent details
GET /tasks                     # Pending tasks
GET /tasks/{id}                # Task status
POST /execute                  # Execute swarm cycle
GET /stats                     # System statistics
```

#### Agent Architecture

Base agent class:

```python
class Agent:
    name: str                          # Agent identifier
    description: str                   # What it does
    capabilities: List[str]            # Supported task types
    priority: int                      # Execution priority
    
    def execute(self, task: Task) -> Dict: # Execute task
        pass
    
    def validate(self, payload: Dict) -> bool: # Validate input
        pass
```

**Available Agents**:

1. **Coordinator** - Multi-agent orchestration
   - Schedules tasks across agents
   - Coordinates dependencies
   - Manages resource allocation

2. **TerrainGenerator** - Terrain generation
   - Generates procedural terrain
   - Applies erosion and features
   - Exports heightmaps

3. **WeatherSimulator** - Weather modeling
   - Simulates weather systems
   - Calculates environmental effects
   - Updates world state

4. **PhysicsSimulator** - Physics calculations
   - Runs physics iterations
   - Detects collisions
   - Applies forces

#### Task Queue System

```python
class TaskQueue:
    def enqueue(self, agent_id, agent_role, task_type, payload)
    def get_pending_tasks(self) -> List[Task]
    def get_task(self, task_id: str) -> Task
    def update_task(self, task_id, status, result)
    def stats(self) -> Dict
```

Task states: `pending` → `running` → `completed` (or `failed`)

### 6. Data Persistence (`prisma/`)

Prisma ORM schema with these models:

**Agent** - Active agents
- Fields: `id`, `role`, `status`, `createdAt`, `updatedAt`
- Relations: `tasks[]`, `logs[]`

**Task** - Work items
- Fields: `id`, `agentId`, `type`, `payload`, `status`, `result`, `retries`
- Relations: `agent`, `logs[]`

**SimulationState** - State snapshots
- Fields: `id`, `timestamp`, `data`, `version`

**WorldState** - Current world
- Fields: `id`, `state`, `timestamp`

**ExecutionLog** - Action logs
- Fields: `id`, `agentId`, `taskId`, `action`, `result`, `success`, `timestamp`

**AgentMetrics** - Performance data
- Fields: `id`, `agentId`, `tasksCompleted`, `tasksFailed`, `avgExecutionMs`

**Checkpoint** - Simulation checkpoints
- Fields: `id`, `name`, `description`, `data`, `timestamp`

## Communication Patterns

### Request/Response (REST)

```
Client → Express Server → Database
  ↓
  Response with data/status
```

### Real-time Updates (WebSocket)

```
Client ⟷ Express Server
  ↑
  Published events (world updates, sim state)
```

### Asynchronous Tasks (Orchestrator)

```
Client → Orchestrator
  ↓
  Task enqueued
  ↓
  Agent processes
  ↓
  Result stored in database
```

### IPC (Memory Files)

```
Express ↔ Orchestrator (via memory/ directory)
  - world_state.json (shared state)
  - tasks_queue.json (sync point)
  - agents.json (registry)
```

## Data Flow

### Simulation Cycle

```
1. Client sends start command
   ↓
2. Express receives /api/sim/start
   ↓
3. Simulation engine initializes
   ↓
4. Physics/Earth/Space engines run
   ↓
5. Results stored in database
   ↓
6. WebSocket broadcasts updates
   ↓
7. Clients receive updates
```

### Agent Task Execution

```
1. Client submits task via POST /execute
   ↓
2. Orchestrator enqueues task
   ↓
3. Agent picks up task from queue
   ↓
4. Agent validates input
   ↓
5. Agent executes logic
   ↓
6. Results stored in database
   ↓
7. Client polls GET /tasks/{id} for status
```

### Offline Operation

```
1. Client sends command (offline)
   ↓
2. Express queues in offline_queue table
   ↓
3. Command marked with expiry (30 days)
   ↓
4. Connection restored
   ↓
5. Sync endpoint processes queue
   ↓
6. Results merged with server state
   ↓
7. Queue cleared
```

## Concurrency & Threading

- **Node.js**: Event loop handles thousands of concurrent connections
- **Python**: FastAPI with ASGI for async operations
- **Database**: SQLite WAL mode supports concurrent reads
- **Recommendations**:
  - Use worker threads for CPU-intensive physics
  - Enable Redis for distributed caching
  - Implement connection pooling for PostgreSQL

## Performance Characteristics

### Latency (Codespaces benchmarks)

| Operation | Time |
|-----------|------|
| Server startup | ~2s |
| Database ready | ~1s |
| Health check | <100ms |
| REST API response | 50-200ms |
| Terrain generation (256x256) | ~500ms |
| Physics update (100 bodies) | ~50ms |
| Asset streaming (1MB) | ~100ms |

### Throughput

- Concurrent connections: 1000+ WebSocket
- REST API: 100+ req/s (single instance)
- Orchestrator: 10+ concurrent agents

### Memory Usage

- Server process: ~100MB baseline
- Per connection (WebSocket): ~1MB
- Database cache: ~50MB for 1000 worlds
- Assets in memory: Configurable (LRU)

## Extensibility Points

### Adding New Simulation Engines

1. Create `backend/sim/custom.js`
2. Implement interface: `start()`, `update()`, `getState()`
3. Add route in `backend/api/sim.js`
4. Expose via REST API

### Adding New Agents

1. Create `orchestrator/agents/custom_agent.py`
2. Extend `Agent` base class
3. Register in `orchestrator/agents/__init__.py`
4. Submit tasks via `/execute` endpoint

### Adding New Endpoints

1. Create route in `backend/api/`
2. Add to `server.js` with `app.use()`
3. Document in `docs/API.md`
4. Add corresponding database operations

### Database Schema Extensions

1. Edit `prisma/schema.prisma`
2. Create migration: `prisma migrate dev --name feature`
3. Update models in `backend/db/models.js`
4. Update API endpoints to use new fields

## Security Architecture

### Current Implementation

- Local development mode
- Basic input validation
- SQLite database (no encryption yet)
- No TLS/SSL by default

### Recommended for Production

1. **Authentication**: OAuth 2.0 or JWT
2. **Encryption**: SQLite encryption, TLS/SSL
3. **Authorization**: Role-based access control (RBAC)
4. **Secrets**: GitHub Secrets for API keys
5. **Logging**: Audit trails for all actions
6. **Rate Limiting**: Per-endpoint protection
7. **Input Validation**: Comprehensive validation
8. **API Keys**: Rotation and revocation

See `docs/SECURITY.md` for details.

## Deployment Topology

### Single Instance (Development)

```
All services on one machine
- Express (port 3000)
- Orchestrator (port 8000)
- SQLite database
- External drives (optional)
```

### Multi-Instance (Production)

```
Load Balancer
  ├── Express Instance 1
  ├── Express Instance 2
  └── Express Instance N
  
Shared PostgreSQL Database
Shared Redis Cache
Orchestrator Cluster (Python workers)
```

See `docs/DEPLOYMENT.md` for scaling details.

## Integration Points

### iOS App Integration

Uses Bluetooth Low Energy (BLE):
- Device discovery via characteristic scanning
- Commands sent as BLE writes
- State updates via characteristic notifications
- Offline command queueing in app

### External Tools

REST API supports:
- JavaScript/Node.js clients
- Python clients
- cURL commands
- Any HTTP client

### Cloud Integration

Ready for:
- Firebase Realtime Database
- Google Cloud Firestore
- AWS DynamoDB
- Custom cloud backends

## Development Workflow

```
1. Clone repository
2. Install dependencies: npm ci, pip install
3. Set environment variables
4. Run migrations: npm run db:migrate
5. Start development: npm run dev
6. Make changes
7. Run tests: npm test
8. Commit changes
9. Push to branch
10. Create pull request
11. CI/CD validates
12. Deploy to main
```

## Monitoring & Observability

### Health Endpoints

```bash
# Backend health
curl http://localhost:3000/health

# Orchestrator health
curl http://0.0.0.0:8000/health

# System stats
curl http://0.0.0.0:8000/stats
```

### Debug Logging

```bash
# All modules
DEBUG=omniverse:* npm run dev

# Specific module
DEBUG=omniverse:sim:* npm run dev
DEBUG=omniverse:portable npm run dev
```

### Database Inspection

```bash
# SQLite shell
sqlite3 data/omniverse.db

# View schema
.schema

# Query worlds
SELECT * FROM world_state;
```

## Future Architecture Enhancements

1. **Microservices**: Break into independent services
2. **Message Queue**: Use RabbitMQ/Kafka for async tasks
3. **Distributed Cache**: Add Redis/Memcached
4. **CDN**: Host assets on CDN for faster delivery
5. **WebGL Rendering**: Web-based visualization
6. **Real-time Collaboration**: Multiplayer support
7. **Machine Learning**: Integrate trained models
8. **GraphQL**: Alternative to REST API

---

For implementation details, see:
- `docs/API.md` - REST endpoint specification
- `docs/PRISMA_SCHEMA.md` - Database model details
- `docs/HF_SWARM_GUIDE.md` - Orchestrator deep dive
- `docs/DEPLOYMENT.md` - Production setup
