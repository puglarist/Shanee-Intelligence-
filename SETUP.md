# Omniverse Engine MVP Setup Guide

## Overview

This is the Phase 1 foundation of the Omniverse Intelligence Engine - a self-running AI orchestration kernel built on Hugging Face integration and autonomous world simulation.

## Architecture

```
/memory                    - Persistent world state
/orchestrator             - Core execution loop
/hf                       - Hugging Face integration
/simulation/earth         - Earth simulation system
/logs                     - Execution logs (auto-generated)
/tasks                    - Task queue (auto-generated)
```

## Core Components

### 1. Orchestrator Engine (`orchestrator/engine.js`)
- Main execution loop
- Runs iterations at configurable intervals
- Manages world state persistence
- Coordinates all subsystems

### 2. Task Generator (`orchestrator/task_generator.js`)
- Generates varied tasks based on world state
- Tasks include: climate updates, biome evolution, terrain generation, city development, economy simulation, narrative generation
- Dynamic task prioritization

### 3. Role Dispatcher (`orchestrator/role_dispatcher.js`)
- Assigns roles from 2,500-role registry
- 800+ Earth simulation roles
- 700+ Civilization system roles
- 300+ Stronghold roles
- 400+ Cinematic roles
- 200+ Game mechanics roles
- 100+ iOS control roles

### 4. HF Integration (`hf/integration.js`)
- Supports two modes:
  - **mock**: Local testing with synthetic outputs
  - **production**: Real Hugging Face API calls
- Automatic fallback to mock if API key missing
- Task-to-prompt conversion
- Response parsing

### 5. Earth Simulation (`simulation/earth/generator.js`)
- Climate modeling (temperature, CO2, sea level)
- Biome generation and evolution
- City creation and growth
- Terrain generation
- Structured JSON output

## Quick Start

### Installation

```bash
npm install
```

### Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key settings:
- `ITERATION_INTERVAL`: Time between execution cycles (default: 5000ms)
- `HF_MODE`: "mock" or "production"
- `HF_API_KEY`: Hugging Face API key (production mode)
- `NODE_ENV`: "development" or "production"

### Running the Engine

```bash
npm start
```

This will:
1. Load world state from `/memory/world_state.json`
2. Begin autonomous execution loop
3. Generate tasks
4. Assign roles
5. Process via HF (or mock)
6. Run Earth simulation
7. Update world state
8. Persist changes
9. Repeat on interval

### Monitoring

View live logs:
```bash
npm run logs
```

Check world state evolution:
```bash
cat memory/world_state.json
```

## Execution Flow

Each iteration:

```
PHASE 1: Generate Tasks (3-6 tasks)
  ↓
PHASE 2: Assign Roles (from 2,500-role registry)
  ↓
PHASE 3: Process via HF/Mock
  ↓
PHASE 4: Run Earth Simulation
  ↓
PHASE 5: Update World State
  ↓
PHASE 6: Persist to Disk
  ↓
[Wait for next interval]
```

## Observable Outputs

### Logs
- `logs/execution.log` - Complete execution trace

### Memory Files
- `memory/world_state.json` - Current world state
- `memory/agent_roles.json` - 2,500-role registry
- `memory/decision_log.json` - Historical decisions

### Key Metrics to Watch
- `world_state.earth.age_cycles` - Simulation age
- `world_state.earth.climate_state` - Temperature, CO2, sea level
- `world_state.earth.cities` - City count and populations
- `world_state.execution_metrics` - Task counts and iteration count

## Example World State Evolution

**Iteration 0:**
- Temperature: 15.2°C
- Cities: 0
- Age: 0 cycles

**Iteration 10:**
- Temperature: 15.3-15.5°C
- Cities: 1-2 (New Haven, Rising Springs)
- Age: 10 cycles
- Biomes: Forest, Grassland

**Iteration 50:**
- Temperature: 15.4-16.2°C
- Cities: 5-10 with growing populations
- Age: 50 cycles
- Regions: Multiple terrain features

## Production Readiness

This MVP includes:
- ✅ Self-contained execution loop
- ✅ Observable world evolution
- ✅ Memory persistence
- ✅ 2,500-role system (config-based)
- ✅ HF integration with mock mode
- ✅ Earth simulation with climate/biome/city systems
- ✅ Complete logging and tracing

## Next Steps (Phase 2+)

1. **Observability**: Web dashboard showing world evolution
2. **Stronghold System**: Protected world architecture
3. **Cinematic Systems**: Story and narrative generation
4. **iOS Control**: SwiftUI-based control interface
5. **Multiplayer**: Distributed simulation infrastructure
6. **Unreal Integration**: Render world in UE5

## Performance Notes

- Mock mode: ~50-100ms per iteration
- Production mode: ~500ms-2s per iteration (depends on HF API)
- Memory usage: ~50MB baseline + growth with iterations
- Logs grow ~100KB per 100 iterations

## Troubleshooting

**Engine hangs on startup:**
- Check `/memory` directory exists and is writable
- Check `.env` file exists

**HF API errors:**
- Verify `HF_API_KEY` is valid (production mode)
- Set `HF_MODE=mock` to bypass API

**Missing logs:**
- Ensure `/logs` directory is writable
- Check `chmod` permissions

## Architecture Philosophy

This system is built as a **foundation-first** incremental architecture:
- Core orchestration layer enables everything else
- Real world evolution through one functioning system (Earth)
- Observable outputs validate design choices
- Scales incrementally to full Omniverse

The 2,500-role system is config-only at this phase - roles guide task generation and provide intelligence structure, but execution happens through HF + simulation layers.
