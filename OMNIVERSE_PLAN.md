# Portable Omniverse Engine - Implementation Plan

## EXECUTIVE SUMMARY
Build a complete, production-ready Omniverse Engine that:
- Runs natively on GitHub Codespaces
- Operates offline-first with optional cloud sync
- Supports external drive portability via iOS Bluetooth
- Provides modular architecture for extensibility
- Delivers realistic Earth and space simulations

---

## PHASE 1: DETAILED SCOPE

### 1.1 GitHub Codespaces Infrastructure
**Deliverables:**
- `.devcontainer/devcontainer.json` - Full Dev Container config
- `docker-compose.yml` - Multi-service orchestration
- `.devcontainer/Dockerfile` - Custom container image
- `scripts/bootstrap.sh` - Environment initialization
- Health check endpoints and startup validation

**Success Criteria:**
- Container builds in < 5 minutes
- All services start without errors
- Health check endpoint responds 200 OK
- Environment variables properly configured

### 1.2 Portable Backend Runtime
**Deliverables:**
- Node.js Express server (REST API + WebSocket)
- SQLite database layer with migrations
- Path remapping system for external drives
- Modular package loader
- Asset streaming and caching
- Offline queue management

**Components:**
```
backend/
├── server.js              # Entry point
├── api/
│   ├── world.js          # World state endpoints
│   ├── assets.js         # Asset streaming
│   ├── sim.js            # Simulation control
│   └── sync.js           # Cloud sync API
├── db/
│   ├── models.js         # Data models
│   ├── migrations/       # Database migrations
│   └── sqlite.db         # Portable database
├── sim/
│   ├── earth.js          # Earth simulation
│   ├── space.js          # Space simulation
│   ├── terrain.js        # Terrain generation
│   ├── physics.js        # Physics engine
│   └── ai.js             # AI agents
├── storage/
│   ├── portable.js       # Path remapping
│   ├── modular.js        # Package system
│   └── cache.js          # Asset caching
└── config/
    ├── defaults.js       # Configuration
    └── local.js          # Local overrides
```

### 1.3 iOS Bluetooth Remote Control App
**Deliverables:**
- Native Swift iOS app with SwiftUI
- CoreBluetooth integration
- Device discovery protocol
- Pairing mechanism
- Command synchronization
- Real-time state display
- Offline command queue

**Screens:**
- Device discovery/pairing screen
- Real-time simulation control
- World state viewer
- Settings/configuration
- Offline queue status

### 1.4 Simulation Frameworks

#### Earth Simulation
- Terrain generation (procedural/heightmap)
- Weather simulation
- Day/night cycle
- Atmospheric effects
- Real-world geographic data

#### Space Simulation
- Orbital mechanics (Kepler equations)
- Celestial body rendering
- Spacecraft dynamics
- Satellite tracking
- Solar system model

#### Physics & Rendering
- 3D rendering engine (Three.js/Babylon.js)
- Physics simulation (Cannon.js)
- Particle effects
- Collision detection
- Lighting and shadows

### 1.5 Modular Package Architecture
**Package Structure:**
```
packages/
├── core/              # Core engine
├── sim-earth/         # Earth simulation
├── sim-space/         # Space simulation
├── renderer/          # Rendering pipeline
├── physics/           # Physics engine
├── assets/            # Asset management
├── bluetooth/         # Bluetooth protocol
└── offline/           # Offline support
```

Each package is:
- Self-contained and independently loadable
- Version-managed
- Dependency-transparent
- Offline-capable
- Remotely patchable

---

## PHASE 2: 5-ANGLE ADVERSARIAL CRITIQUE

### CRITIC 1: SCOPE REALISM
**Question:** Is this scope achievable in one pass?

**Critique:**
- iOS app requires Xcode/Mac environment - may not be compatible with web-only workflow
- Simulation frameworks (terrain, orbital mechanics) are complex - may need simplification
- External drive + Bluetooth integration is novel - untested architecture
- DevContainer is straightforward but multi-service Docker Compose adds complexity

**Recommendation:**
- Focus DevContainer and backend as Phase 1
- Create iOS app prototype/skeleton (architecture, not full implementation)
- Use simplified simulation frameworks with expansion points
- External drive support through standard path configuration first
- Plan iOS/Simulation expansion in follow-up phases

### CRITIC 2: SIMPLICITY & MAINTAINABILITY
**Question:** Can a single developer maintain this?

**Critique:**
- 5 distinct technology stacks (DevContainer, Node.js, Swift, 3D rendering, Bluetooth)
- Complex offline-sync mechanism is error-prone
- Modular package system adds architectural overhead
- Database migrations and persistence require careful design

**Recommendation:**
- Keep backend and frontend communication simple (REST + WebSocket)
- Use battle-tested libraries (Express, SQLite, Three.js)
- Defer complex offline-sync to Phase 2
- Use straightforward modular pattern (plugin directory scanning)
- Document architecture extensively

### CRITIC 3: CODE REUSE & PATTERNS
**Question:** What can we reuse from existing systems?

**Critique:**
- DevContainer patterns are standard - use existing templates
- Node.js patterns are well-established (Express servers)
- SQLite has proven migration tools
- Three.js/Babylon.js examples are abundant
- Bluetooth protocol can follow established discovery/pairing patterns

**Recommendation:**
- Clone DevContainer templates from Microsoft/Google
- Use Express best practices (middleware, error handling)
- Leverage Knex.js for database migrations
- Use Three.js examples as simulation baseline
- Follow BLE GATT standard for Bluetooth protocol

### CRITIC 4: VERIFICATION & TESTING
**Question:** How do we verify this works end-to-end?

**Critique:**
- Codespaces environment is cloud-based - can't test external drive locally
- iOS app requires physical device or simulator
- Simulation frameworks need visual verification
- Bluetooth requires paired devices to test
- Offline operation needs intentional disconnection testing

**Recommendation:**
- Unit tests for backend API and database layer
- Integration tests for DevContainer startup
- Mock Bluetooth protocol for testing (before iOS app)
- Simulation framework with test data and visual inspection
- Document manual testing procedures for external drive and iOS
- Use GitHub Actions for CI/CD with available test matrix

### CRITIC 5: CORRECTNESS & PRODUCTION QUALITY
**Question:** What will break in production?

**Critique:**
- Path remapping might fail on different OSes (Windows vs Linux vs macOS)
- SQLite doesn't handle concurrent writes well - could corrupt data
- Bluetooth pairing is stateful - easy to lose sync
- External drive might become unmounted - graceful degradation needed
- Offline queue could grow unbounded - needs cleanup policy
- Asset streaming could OOM with large files - needs chunking

**Recommendation:**
- Cross-platform path handling (use path module, not hardcoded separators)
- Use WAL (Write-Ahead Logging) mode for SQLite
- Implement Bluetooth state machine with explicit transitions
- Monitor drive connectivity, fallback to local storage
- Implement queue with size limits and expiration
- Stream large assets in chunks with progress reporting
- Add comprehensive error handling and recovery

---

## PHASE 3: HARDENED IMPLEMENTATION PLAN

### Priority 1: DevContainer Infrastructure (Days 1-2)
1. Create `.devcontainer/devcontainer.json` with:
   - Node.js base image (node:20-bullseye)
   - Required system dependencies (SQLite dev tools, build-essential)
   - Git and common tools
   - Port forwarding configuration

2. Create `docker-compose.yml` with:
   - Backend service (Node.js)
   - SQLite service (optional, embedded for portability)
   - Dev server with hot-reload
   - Volume mounts for code

3. Create `scripts/bootstrap.sh`:
   - Initialize database
   - Install dependencies (npm)
   - Seed with test data
   - Run health checks

### Priority 2: Portable Backend (Days 3-5)
1. Create basic Node.js/Express server with:
   - Health check endpoint (/health)
   - World state API (/api/world/*)
   - Asset streaming (/api/assets/*)
   - WebSocket for real-time updates

2. Implement SQLite layer:
   - Schema for world state
   - Asset metadata storage
   - Sync history tracking
   - Database initialization

3. Implement portable storage:
   - Path remapping system for external drives
   - Asset caching with TTL
   - Offline queue management
   - Disk space monitoring

### Priority 3: iOS Bluetooth App (Days 6-8)
1. Create Swift project structure with:
   - CoreBluetooth integration
   - GATT service definitions
   - Device discovery
   - Pairing flow

2. Implement UI:
   - Device discovery screen
   - Connected device status
   - Command interface (simplified)
   - Offline queue indicator

3. Implement protocol:
   - BLE advertisement format
   - Command serialization
   - State synchronization
   - Error handling

### Priority 4: Simulation Foundation (Days 9-11)
1. Create Earth simulation module:
   - Simple procedural terrain
   - Day/night cycle
   - Basic atmosphere

2. Create Space simulation module:
   - Simple orbital mechanics
   - Solar system model
   - Celestial body rendering

3. Integrate rendering:
   - Three.js scene setup
   - Camera controls
   - Basic lighting

### Priority 5: Integration & Testing (Days 12-14)
1. End-to-end testing:
   - DevContainer startup verification
   - Backend + database integration
   - iOS app connection flow
   - Simulation rendering

2. Documentation:
   - Architecture overview
   - DevContainer usage guide
   - iOS app build instructions
   - API reference

3. Quality assurance:
   - Code review
   - Performance profiling
   - Error case testing
   - Documentation verification

---

## PHASE 4: SUCCESS CRITERIA (HARDENED)

### DevContainer
- [ ] Container builds successfully
- [ ] All services start without errors
- [ ] Health check endpoint responds 200 OK
- [ ] Hot-reload works for code changes
- [ ] Port forwarding enables local development

### Backend
- [ ] Server starts without errors
- [ ] Database initialization succeeds
- [ ] API endpoints return correct responses
- [ ] WebSocket connections establish
- [ ] Asset streaming works
- [ ] Offline queue persists and syncs

### iOS App
- [ ] App compiles and runs on simulator
- [ ] Device discovery works
- [ ] Pairing protocol completes
- [ ] Commands send successfully
- [ ] State updates in real-time
- [ ] Offline queue displays

### Simulation
- [ ] Engine initializes without errors
- [ ] Terrain renders without glitches
- [ ] Orbital mechanics calculate correctly
- [ ] Camera controls respond smoothly
- [ ] No memory leaks on extended run

### Overall
- [ ] All modules work offline
- [ ] External drive mounting detected
- [ ] Path remapping works across OSes
- [ ] API documentation complete
- [ ] Code passes linting
- [ ] TypeScript definitions included

---

## TECHNICAL DECISIONS (LOCKED)

1. **Backend Language:** Node.js/Express
   - Reason: Codespaces-friendly, fast development
   
2. **Database:** SQLite with WAL mode
   - Reason: Portable, no server dependencies, offline-capable

3. **iOS Development:** Swift with SwiftUI
   - Reason: Native Bluetooth APIs, modern language

4. **Rendering:** Three.js
   - Reason: Widely-used, good documentation, portable

5. **Package Format:** Standard npm packages with custom loader
   - Reason: Familiar to Node developers, versioning built-in

6. **DevContainer:** Microsoft standard format
   - Reason: Native Codespaces support, reproducible

---

## RISKS & MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| iOS app requires Mac to build | High | Medium | Create build instructions, use Xcode Cloud |
| Bluetooth pairing unreliable | Medium | High | Implement robust state machine, add reconnection logic |
| External drive unmounting | Medium | High | Monitor mount status, graceful degradation to local |
| SQLite corruption under load | Low | Critical | Enable WAL mode, implement recovery |
| Path portability issues | Medium | Medium | Use path module, cross-platform testing |
| Asset streaming memory issues | Low | High | Implement chunking, add progress reporting |

---

## DELIVERABLES CHECKLIST

### DevContainer & Infrastructure
- [ ] `.devcontainer/devcontainer.json`
- [ ] `.devcontainer/Dockerfile`
- [ ] `docker-compose.yml`
- [ ] `scripts/bootstrap.sh`
- [ ] `scripts/health-check.js`

### Backend
- [ ] `backend/server.js`
- [ ] `backend/api/world.js`
- [ ] `backend/api/assets.js`
- [ ] `backend/db/models.js`
- [ ] `backend/db/sqlite.db`
- [ ] `backend/sim/earth.js`
- [ ] `backend/sim/space.js`
- [ ] `backend/storage/portable.js`
- [ ] `backend/package.json`

### iOS App
- [ ] `ios/OmniverseControl/OmniverseControl.xcodeproj`
- [ ] `ios/OmniverseControl/ContentView.swift`
- [ ] `ios/OmniverseControl/BluetoothManager.swift`
- [ ] `ios/OmniverseControl/DeviceDiscovery.swift`

### Documentation
- [ ] `README.md` (project overview)
- [ ] `ARCHITECTURE.md` (system design)
- [ ] `DEVCONTAINER.md` (setup guide)
- [ ] `API.md` (endpoint documentation)
- [ ] `CONTRIBUTING.md` (development guide)

---

## NEXT PHASE: IMPLEMENTATION

Once this plan is approved, proceed to PHASE 2: IMPLEMENT with single-agent execution of hardened plan.

