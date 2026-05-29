# Getting Started with Omniverse Engine

Quick-start guide for all user types: beginners, developers, and DevOps engineers.

## For Beginners: 3-Minute Setup

### Option 1: GitHub Codespaces (Recommended)

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait for container to build (first time: ~5 minutes)
3. Terminal opens automatically

```bash
cd backend && npm run dev
```

Visit `http://localhost:3000/health` - you should see:
```json
{
  "status": "healthy",
  "uptime": 2.3,
  "database": "ready",
  "services": ["api", "simulator", "assets"]
}
```

### Option 2: Local Docker (5 minutes)

```bash
# Clone the repository
git clone https://github.com/puglarist/Shanee-Intelligence-.git
cd Shanee-Intelligence-

# Start with Docker Compose
docker-compose up

# In another terminal
npm run bootstrap
cd backend && npm run dev
```

### Option 3: Direct Installation (10 minutes)

Requirements:
- Node.js 20+ (download from [nodejs.org](https://nodejs.org))
- SQLite3 (included on most systems)

```bash
cd backend
npm ci
npm run db:migrate
npm run dev
```

## For Developers: Running & Extending

### Project Structure

```
backend/
├── api/              # REST endpoint definitions
│   ├── world.js      # World state management
│   ├── assets.js     # Asset discovery & streaming
│   ├── sim.js        # Simulation control
│   └── sync.js       # Offline sync & queueing
├── sim/              # Simulation engines
│   ├── earth.js      # Earth/terrain simulation
│   ├── space.js      # Orbital mechanics
│   └── physics.js    # Rigid body dynamics
├── core/             # Core utilities
│   ├── portable_runtime.js  # Cross-platform paths
│   └── asset_manager.js     # Asset handling
├── db/               # Database layer
│   ├── models.js     # Data models
│   ├── schema.sql    # Database schema
│   ├── migrate.js    # Schema initialization
│   └── seed.js       # Initial data
└── server.js         # Express server entry

orchestrator/        # Python FastAPI orchestrator
├── main.py          # REST API server
├── agents/          # AI agent definitions
│   ├── coordinator.py       # Multi-agent coordinator
│   └── earth_sim.py         # Earth simulation agent
├── tasks/           # Task queue management
│   └── queue.py     # Task scheduling
└── config.py        # Configuration

prisma/             # Data persistence layer
├── schema.prisma   # ORM schema definition
└── migrations/     # Migration history
```

### Running the Backend

```bash
# Development mode (with auto-reload)
cd backend
npm run dev

# Watch mode (for testing)
npm test -- --watch

# With specific debug output
DEBUG=omniverse:* npm run dev
```

### Running the Orchestrator

```bash
# Mock mode (no API key required)
HF_API_KEY=mock python orchestrator/main.py

# With Hugging Face API
HF_API_KEY=your-key python orchestrator/main.py

# Access the API
curl http://0.0.0.0:8000/health
```

### Creating Your First Simulation

Here's how to create a custom Earth simulation scenario:

```javascript
// backend/api/sim.js
const { EarthSim } = require('../sim/earth');

// Create instance
const earth = new EarthSim({
  seed: 42,
  resolution: 512,
  weather: {
    windSpeed: 15,
    temperature: 20,
    humidity: 0.65
  }
});

// Generate terrain
const terrain = earth.generateTerrain();

// Get weather at location
const weather = earth.getWeatherAt(latitude, longitude);

// Advance time
earth.updateDayNightCycle(3600000); // 1 hour
```

### Creating a Custom Agent

1. Create your agent in `orchestrator/agents/`:

```python
# orchestrator/agents/custom_agent.py
from orchestrator.agents import Agent

class CustomAgent(Agent):
    """Your custom agent implementation."""
    
    name = "CustomAgent"
    description = "Does something awesome"
    capabilities = ["task_type_1", "task_type_2"]
    priority = 5
    
    def execute(self, task):
        """Execute task and return result."""
        payload = task.payload
        # Your logic here
        return {
            "status": "success",
            "result": "..."
        }
```

2. Register it in `orchestrator/agents/__init__.py`:

```python
from .custom_agent import CustomAgent

AGENTS = [
    # ... existing agents ...
    CustomAgent(),
]
```

3. Submit a task:

```bash
curl -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "CustomAgent",
    "task_type": "task_type_1",
    "payload": { "your": "data" }
  }'
```

## For DevOps: Deployment & Scaling

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Key variables:

```bash
# Backend
PORT=3000                                    # Server port
NODE_ENV=production                          # development|production
DEBUG=                                       # debug:* for verbose logging

# Database
DATABASE_URL=file:./data/omniverse.db       # SQLite path
DATABASE_PROVIDER=sqlite                    # sqlite|postgresql

# External Storage
EXTERNAL_DRIVE_PATH=/media/usb             # Auto-detected if not set
EXTERNAL_DRIVE_ENABLED=true

# Orchestrator (Python)
HF_API_KEY=your-hugging-face-key           # Hugging Face API token
HF_MODEL_ENDPOINT=https://api-inference... # Custom endpoint
ORCHESTRATOR_PORT=8000
ORCHESTRATOR_HOST=0.0.0.0
```

### Docker Deployment

```bash
# Build Docker image
docker build -t omniverse-engine:latest .

# Run container
docker run -p 3000:3000 \
  -e DATABASE_URL=/app/data/db.sqlite \
  -e PORT=3000 \
  -v ./data:/app/data \
  omniverse-engine:latest
```

### GitHub Codespaces Production Setup

```bash
# Build container
docker-compose build

# Start services
docker-compose up

# Verify health
curl http://localhost:3000/health

# Check logs
docker-compose logs -f backend
```

### Monitoring Health

```bash
# Simple health check
curl http://localhost:3000/health

# Database status
curl http://localhost:3000/api/world/states

# Get system stats
curl http://0.0.0.0:8000/stats

# List agents
curl http://0.0.0.0:8000/agents
```

### Scaling Considerations

1. **Horizontal Scaling**: Run multiple instances behind a load balancer
2. **Database**: Switch from SQLite to PostgreSQL for concurrent writes
3. **Caching**: Enable Redis for asset caching
4. **Orchestrator**: Scale Python workers with worker pools

See `docs/DEPLOYMENT.md` for detailed instructions.

## Testing

### Unit Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch

# Specific test file
npm test -- sim.test.js
```

### Integration Tests

```bash
# Test backend + database
npm run test:integration

# Test orchestrator
pytest orchestrator/tests/
```

### Load Testing

```bash
# Using built-in health check
for i in {1..100}; do
  curl http://localhost:3000/health
done
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs backend

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up
```

### Database locked

```bash
# Reset database
rm -rf data/
npm run db:migrate
npm run db:seed
npm run dev
```

### Port already in use

```bash
# Change port in .env
echo "PORT=3001" >> .env
npm run dev

# Or kill the existing process
lsof -i :3000 | grep -v PID | awk '{print $2}' | xargs kill -9
```

### Orchestrator won't connect

```bash
# Check if it's running
ps aux | grep python

# Test connection
curl http://0.0.0.0:8000/health

# View logs
cat memory/*.json | tail -20
```

## Next Steps

1. **Read**: `docs/SYSTEM_ARCHITECTURE.md` - Understand the full system
2. **Explore**: Visit http://localhost:3000 and try the API
3. **Customize**: Create your own agents and simulations
4. **Deploy**: Follow `docs/DEPLOYMENT.md` for production

## Quick API Examples

### Get World State

```bash
curl http://localhost:3000/api/world/default
```

### Start Simulation

```bash
curl -X POST http://localhost:3000/api/sim/start \
  -H "Content-Type: application/json" \
  -d '{ "world_name": "default" }'
```

### Subscribe to Updates via WebSocket

```javascript
const ws = new WebSocket('ws://localhost:3000/ws/updates');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    clientId: 'client-1',
    subscriptions: ['world', 'simulation']
  }));
};

ws.onmessage = (event) => {
  console.log('Update:', JSON.parse(event.data));
};
```

### List Available Agents

```bash
curl http://0.0.0.0:8000/agents
```

### Execute a Task

```bash
curl -X POST http://0.0.0.0:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_role": "TerrainGenerator",
    "task_type": "generate",
    "payload": { "seed": 42, "size": 256 }
  }'
```

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/puglarist/Shanee-Intelligence-/issues)
- **Documentation**: See `docs/` directory
- **Examples**: Check `examples/` directory
- **Community**: [GitHub Discussions](https://github.com/puglarist/Shanee-Intelligence-/discussions)

---

Ready to dive deeper? Check out `docs/SYSTEM_ARCHITECTURE.md` next!
