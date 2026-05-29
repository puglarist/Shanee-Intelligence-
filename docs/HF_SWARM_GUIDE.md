# HF Swarm Orchestrator Guide

Complete reference for using the Hugging Face Swarm orchestrator system for distributed AI-driven simulations.

## Overview

The FastAPI orchestrator coordinates a swarm of AI agents to manage complex simulation tasks:

```
┌─────────────────────────────────────────┐
│     Client (REST API Client)             │
│     e.g., curl, Python, JavaScript      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   FastAPI Orchestrator Server           │
│   http://0.0.0.0:8000                   │
├─────────────────────────────────────────┤
│  Agent Management                       │
│  ├── TerrainGenerator                   │
│  ├── WeatherSimulator                   │
│  ├── PhysicsSimulator                   │
│  └── Coordinator                        │
├─────────────────────────────────────────┤
│  Task Queue                             │
│  ├── Pending Tasks                      │
│  ├── Running Tasks                      │
│  └── Completed Tasks                    │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼────────┐  ┌─────▼──────────┐
│ Memory Store   │  │ Prisma ORM     │
│ (JSON files)   │  │ (SQLite/DB)    │
└────────────────┘  └────────────────┘
```

## Quick Start

### 1. Setup Environment

```bash
# Create .env file with required variables
export HF_API_KEY="hf_your_actual_key_here"  # Get from huggingface.co
export HF_MODEL_ENDPOINT="https://api-inference.huggingface.co"
export ORCHESTRATOR_PORT=8000
export ORCHESTRATOR_HOST=0.0.0.0
```

For testing without a real key:

```bash
export HF_API_KEY="mock"
```

### 2. Start the Orchestrator

```bash
# Install dependencies
pip install -r orchestrator/requirements.txt

# Run the server
python orchestrator/main.py
```

Output:
```
Starting Omniverse Engine Orchestrator
  Agents: 4
  Mock mode: False
  Server: 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Health Check

```bash
curl http://0.0.0.0:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-29T12:34:56.789Z",
  "mode": "production",
  "agents_count": 4,
  "config": {
    "mock_mode": false,
    "has_hf_key": true,
    "has_endpoint": true,
    "debug": false
  }
}
```

## Agent System

### List Available Agents

```bash
curl http://0.0.0.0:8000/agents
```

Response:
```json
[
  {
    "name": "Coordinator",
    "description": "Multi-agent task coordinator",
    "capabilities": ["orchestrate", "schedule", "allocate_resources"],
    "priority": 10
  },
  {
    "name": "TerrainGenerator",
    "description": "Procedural terrain generation",
    "capabilities": ["generate", "erode", "validate"],
    "priority": 5
  },
  {
    "name": "WeatherSimulator",
    "description": "Weather system simulation",
    "capabilities": ["simulate", "forecast", "update_state"],
    "priority": 3
  },
  {
    "name": "PhysicsSimulator",
    "description": "Physics engine simulation",
    "capabilities": ["simulate", "collide_detect", "update_state"],
    "priority": 2
  }
]
```

### Get Agent Details

```bash
curl http://0.0.0.0:8000/agents/TerrainGenerator
```

Response:
```json
{
  "name": "TerrainGenerator",
  "description": "Procedural terrain generation",
  "capabilities": ["generate", "erode", "validate"],
  "priority": 5
}
```

## Task Management

### Submit a Task

```bash
curl -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "TerrainGenerator",
    "task_type": "generate",
    "payload": {
      "seed": 42,
      "size": 256,
      "scale": 1.0,
      "octaves": 6,
      "persistence": 0.5
    }
  }'
```

Response:
```json
{
  "status": "enqueued",
  "task_id": "task_abc123def456",
  "message": "Task created for agent 'TerrainGenerator' with type 'generate'"
}
```

### Check Task Status

```bash
curl http://0.0.0.0:8000/tasks/task_abc123def456
```

Response:
```json
{
  "id": "task_abc123def456",
  "agent_id": "TerrainGenerator_1234567890.123",
  "agent_role": "TerrainGenerator",
  "task_type": "generate",
  "status": "completed",
  "result": {
    "heightmap": [...],
    "biomes": [...],
    "features": {...}
  },
  "created_at": "2026-05-29T12:34:56.789Z",
  "updated_at": "2026-05-29T12:35:12.123Z"
}
```

### List Pending Tasks

```bash
curl http://0.0.0.0:8000/tasks
```

Response:
```json
{
  "stats": {
    "pending": 2,
    "running": 1,
    "completed": 15,
    "failed": 0
  },
  "pending": [
    {
      "id": "task_xyz789",
      "agent_id": "WeatherSimulator_1",
      "agent_role": "WeatherSimulator",
      "task_type": "simulate",
      "status": "pending",
      "created_at": "2026-05-29T12:35:20.000Z",
      "updated_at": "2026-05-29T12:35:20.000Z"
    }
  ]
}
```

## Agent Types & Capabilities

### Coordinator Agent

Orchestrates multi-agent tasks and resource allocation.

**Capabilities**: `orchestrate`, `schedule`, `allocate_resources`

**Example Task**:

```bash
curl -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "Coordinator",
    "task_type": "orchestrate",
    "payload": {
      "world_name": "earth_sim_1",
      "tasks": [
        {
          "agent_role": "TerrainGenerator",
          "task_type": "generate",
          "payload": {"seed": 42, "size": 512}
        },
        {
          "agent_role": "WeatherSimulator",
          "task_type": "simulate",
          "payload": {"world": "earth_sim_1"}
        }
      ]
    }
  }'
```

### TerrainGenerator Agent

Generates procedural terrain with realistic features.

**Capabilities**: `generate`, `erode`, `validate`

**Supported Task Types**:

1. **generate**: Create new terrain
   ```json
   {
     "agent_role": "TerrainGenerator",
     "task_type": "generate",
     "payload": {
       "seed": 42,
       "size": 256,
       "scale": 1.0,
       "octaves": 6,
       "persistence": 0.5,
       "lacunarity": 2.0,
       "min_height": -100,
       "max_height": 5000
     }
   }
   ```

2. **erode**: Apply erosion to existing terrain
   ```json
   {
     "agent_role": "TerrainGenerator",
     "task_type": "erode",
     "payload": {
       "heightmap_id": "hm_123",
       "erosion_strength": 0.7,
       "iterations": 100
     }
   }
   ```

3. **validate**: Validate terrain data
   ```json
   {
     "agent_role": "TerrainGenerator",
     "task_type": "validate",
     "payload": {
       "heightmap_id": "hm_123"
     }
   }
   ```

### WeatherSimulator Agent

Simulates atmospheric conditions and weather systems.

**Capabilities**: `simulate`, `forecast`, `update_state`

**Supported Task Types**:

1. **simulate**: Run weather simulation
   ```json
   {
     "agent_role": "WeatherSimulator",
     "task_type": "simulate",
     "payload": {
       "world_id": "earth_1",
       "location": {"lat": 40.7128, "lon": -74.0060},
       "duration_hours": 24,
       "timestep_minutes": 30
     }
   }
   ```

2. **forecast**: Generate weather forecast
   ```json
   {
     "agent_role": "WeatherSimulator",
     "task_type": "forecast",
     "payload": {
       "world_id": "earth_1",
       "location": {"lat": 40.7128, "lon": -74.0060},
       "days": 7
     }
   }
   ```

3. **update_state**: Update world weather state
   ```json
   {
     "agent_role": "WeatherSimulator",
     "task_type": "update_state",
     "payload": {
       "world_id": "earth_1",
       "weather_data": {
         "temperature": 22.5,
         "humidity": 0.65,
         "wind_speed": 15.2,
         "precipitation": 0.0
       }
     }
   }
   ```

### PhysicsSimulator Agent

Simulates physics and collision detection.

**Capabilities**: `simulate`, `collide_detect`, `update_state`

**Supported Task Types**:

1. **simulate**: Run physics simulation
   ```json
   {
     "agent_role": "PhysicsSimulator",
     "task_type": "simulate",
     "payload": {
       "world_id": "physics_world_1",
       "bodies": [...],
       "duration_seconds": 10,
       "timestep_ms": 16
     }
   }
   ```

2. **collide_detect**: Detect collisions
   ```json
   {
     "agent_role": "PhysicsSimulator",
     "task_type": "collide_detect",
     "payload": {
       "world_id": "physics_world_1"
     }
   }
   ```

3. **update_state**: Update physics state
   ```json
   {
     "agent_role": "PhysicsSimulator",
     "task_type": "update_state",
     "payload": {
       "world_id": "physics_world_1",
       "entities": [...]
     }
   }
   ```

## Configuration

### Environment Variables

```bash
# API Key for Hugging Face
HF_API_KEY=hf_your_key_here
# or use mock for testing
HF_API_KEY=mock

# Model endpoint (optional)
HF_MODEL_ENDPOINT=https://api-inference.huggingface.co

# Server configuration
ORCHESTRATOR_HOST=0.0.0.0
ORCHESTRATOR_PORT=8000

# Debugging
DEBUG=true  # Enable debug logging
```

### Configuration File (`orchestrator/config.py`)

```python
class Config:
    # Hugging Face API
    hf_api_key: str              # API key or 'mock'
    hf_model_endpoint: str       # API endpoint URL
    
    # Server
    host: str = "0.0.0.0"        # Bind address
    port: int = 8000              # Port number
    
    # Behavior
    mock_mode: bool              # Use mock responses
    debug: bool = False           # Debug logging
    
    # Persistence
    use_prisma: bool = True       # Use Prisma ORM
    database_url: str            # Database connection
```

## Mock Mode

For testing without Hugging Face API:

```bash
# Set API key to 'mock'
export HF_API_KEY=mock
python orchestrator/main.py
```

Mock mode will:
- Generate synthetic responses without calling HF API
- Simulate agent execution
- Return realistic task results
- Allow full testing of orchestrator functionality

## Integration with Express Backend

The orchestrator integrates with Express via shared memory:

### Shared Memory Files

```
memory/
├── world_state.json      # Current world state
├── tasks_queue.json      # Task queue snapshot
└── agents.json           # Agent registry
```

### IPC Workflow

```
1. Express receives API request
2. Creates task in Prisma database
3. Writes to memory/tasks_queue.json
4. Orchestrator polls memory/
5. Picks up new tasks
6. Executes agent logic
7. Writes results back to Prisma
8. Updates memory/world_state.json
9. Express reads updated state
10. Returns to client
```

## Performance Tuning

### Concurrency

Default: 1 agent executing per task. To run multiple tasks in parallel:

```python
# In orchestrator/tasks/queue.py
CONCURRENT_TASKS = 4  # Run up to 4 tasks simultaneously
```

### Task Timeout

Set task execution timeout:

```python
TASK_TIMEOUT_SECONDS = 300  # 5 minutes default
```

### Retry Policy

Configure automatic retries:

```python
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
```

## Advanced Usage

### Custom Agent Implementation

Create a new agent:

```python
# orchestrator/agents/my_agent.py
from orchestrator.agents import Agent, AgentRole

class MyAgent(Agent):
    """Custom agent for specific tasks."""
    
    name = "MyAgent"
    description = "Does something custom"
    capabilities = ["custom_task"]
    priority = 5
    
    def execute(self, task):
        """Execute the task."""
        payload = task.payload
        
        # Validate input
        if not self.validate(payload):
            return {"status": "error", "message": "Invalid payload"}
        
        # Execute logic
        result = self._do_something(payload)
        
        # Return result
        return {"status": "success", "result": result}
    
    def validate(self, payload):
        """Validate task payload."""
        return "required_field" in payload
    
    def _do_something(self, payload):
        """Your custom logic."""
        return payload.get("required_field")
```

Register in `orchestrator/agents/__init__.py`:

```python
from .my_agent import MyAgent

AGENTS = [
    # ... existing agents ...
    MyAgent(),
]
```

### Monitoring and Logging

View logs:

```bash
# Start with debug mode
DEBUG=true python orchestrator/main.py

# In another terminal, tail logs
tail -f memory/execution_log.json
```

### Task Chaining

Execute dependent tasks:

```bash
# Create terrain first
TERRAIN_TASK=$(curl -s -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "TerrainGenerator",
    "task_type": "generate",
    "payload": {"seed": 42, "size": 512}
  }' | jq -r '.task_id')

# Wait for terrain completion
while [ $(curl -s http://0.0.0.0:8000/tasks/$TERRAIN_TASK | jq -r '.status') != "completed" ]; do
  sleep 1
done

# Now simulate weather on completed terrain
curl -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "WeatherSimulator",
    "task_type": "simulate",
    "payload": {
      "world_id": "earth_1",
      "terrain_task_id": "'$TERRAIN_TASK'"
    }
  }'
```

## Troubleshooting

### Orchestrator Won't Start

```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip install -r orchestrator/requirements.txt

# Check port availability
lsof -i :8000  # Port 8000 already in use?
```

### Tasks Not Executing

```bash
# Check agent availability
curl http://0.0.0.0:8000/agents

# Check task queue
curl http://0.0.0.0:8000/tasks

# Check logs
tail -f memory/orchestrator.log
```

### Hugging Face API Errors

```bash
# Verify API key
echo $HF_API_KEY

# Test endpoint
curl -H "Authorization: Bearer $HF_API_KEY" \
  https://api-inference.huggingface.co/status/gpt2

# Use mock mode for testing
export HF_API_KEY=mock
python orchestrator/main.py
```

## API Reference

See `docs/API.md` for complete REST endpoint documentation.

Key endpoints:
- `GET /health` - Health check
- `GET /agents` - List agents
- `POST /execute` - Submit task
- `GET /tasks` - List tasks
- `GET /tasks/{id}` - Task status
- `GET /stats` - System statistics

## Examples

### Example 1: Generate Terrain and Simulate Weather

```bash
#!/bin/bash

# Generate terrain
TERRAIN=$(curl -s -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "TerrainGenerator",
    "task_type": "generate",
    "payload": {"seed": 123, "size": 256}
  }' | jq -r '.task_id')

echo "Terrain task: $TERRAIN"

# Wait for completion
while true; do
  STATUS=$(curl -s http://0.0.0.0:8000/tasks/$TERRAIN | jq -r '.status')
  echo "Status: $STATUS"
  [ "$STATUS" == "completed" ] && break
  sleep 2
done

# Get terrain result
TERRAIN_DATA=$(curl -s http://0.0.0.0:8000/tasks/$TERRAIN | jq '.result')

# Simulate weather
WEATHER=$(curl -s -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "WeatherSimulator",
    "task_type": "simulate",
    "payload": {
      "world_id": "world_1",
      "terrain": '$TERRAIN_DATA'
    }
  }' | jq -r '.task_id')

echo "Weather task: $WEATHER"
```

### Example 2: Batch Processing

```bash
#!/bin/bash

# Generate 10 different terrains
for i in {1..10}; do
  TASK=$(curl -s -X POST http://0.0.0.0:8000/execute \
    -H "Content-Type: application/json" \
    -d '{
      "agent_role": "TerrainGenerator",
      "task_type": "generate",
      "payload": {"seed": '$i', "size": 256}
    }' | jq -r '.task_id')
  
  echo "Task $i: $TASK"
done

# Monitor all tasks
while true; do
  STATS=$(curl -s http://0.0.0.0:8000/tasks | jq '.stats')
  echo "Stats: $STATS"
  
  # Break when all tasks complete
  if [ $(echo $STATS | jq '.pending + .running') -eq 0 ]; then
    break
  fi
  
  sleep 5
done
```

## Next Steps

1. **Read**: `docs/HF_INTEGRATION.md` - Setup and security
2. **Learn**: `docs/AGENTS.md` - Creating custom agents
3. **Deploy**: `docs/DEPLOYMENT.md` - Production setup

---

For more details, see:
- `orchestrator/main.py` - Server implementation
- `orchestrator/agents/` - Agent implementations
- `orchestrator/tasks/queue.py` - Task queue
- `.github/workflows/omniverse-orchestrator.yml` - GitHub Actions workflow
