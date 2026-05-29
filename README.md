# Stronghold Genesis AI - Autonomous Omniverse World Generation System

An ambitious AI-driven world generation system powered by open-source LLMs capable of autonomously generating entire universes, civilizations, and persistent simulated environments.

## Project Vision

Create a "Universe Architect" - a multi-agent AI system that continuously generates and evolves realistic digital universes with:

- **Autonomous world generation** - Procedurally generated planets, cities, and civilizations
- **Multi-agent orchestration** - Specialized AI agents collaborating to build coherent worlds
- **Persistent simulations** - Worlds that evolve independently over time
- **Protected Stronghold worlds** - Safe sanctuary environments with self-healing infrastructure
- **Unreal Engine integration** - Real-time visualization and interaction
- **Dynamic event generation** - Quests, conflicts, and narrative events
- **Civilization evolution** - Evolving populations, economies, cultures, and politics

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL + Vector DB (Pinecone/Weaviate)
- **ORM**: SQLAlchemy 2.0 with Alembic migrations
- **AI/LLM**: Hugging Face Transformers + LangChain
- **Frontend**: React 18 + TypeScript (upcoming)
- **Infrastructure**: Docker Compose for local development

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Git

### Development Setup

1. **Clone and enter the repository**
   ```bash
   cd Shanee-Intelligence-
   ```

2. **Copy environment configuration**
   ```bash
   cp .env.example .env
   ```

3. **Start the development environment**
   ```bash
   bash setup.sh
   ```
   
   Or manually:
   ```bash
   # Start Docker containers
   docker-compose up -d
   
   # Wait for PostgreSQL to be ready
   sleep 5
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   alembic upgrade head
   ```

4. **Start the API server**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - API Documentation (Swagger): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
.
├── app/
│   ├── api/              # API route handlers
│   │   ├── health.py     # Health check endpoints
│   │   └── worlds.py     # World management endpoints
│   ├── agents/           # AI agent implementations (Phase 2)
│   ├── generation/       # World generation algorithms (Phase 3)
│   ├── simulation/       # Simulation engine (Phase 4)
│   ├── stronghold/       # Stronghold world system (Phase 5)
│   ├── config.py         # Configuration management
│   ├── db.py             # Database setup and sessions
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic request/response schemas
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   ├── env.py            # Migration environment config
│   └── script.py.mako    # Migration template
├── frontend/             # React frontend (Phase 6, upcoming)
├── tests/                # Test suite
├── docker-compose.yml    # Docker services
├── pyproject.toml        # Project dependencies (Poetry)
├── requirements.txt      # Dependencies for pip
└── alembic.ini          # Alembic configuration
```

## Phase 1 Status: Core Infrastructure ✅

### Completed

- ✅ Project scaffolding (FastAPI, Docker Compose, Python structure)
- ✅ PostgreSQL + Redis setup via Docker
- ✅ Database models (8 core tables):
  - `worlds` - World metadata and generation status
  - `planets` - Planetary data (terrain, biomes, resources)
  - `civilizations` - Civilization state and evolution
  - `locations` - Cities, landmarks, dungeons
  - `npcs` - AI characters with personalities
  - `events` - Generated world events
  - `agent_memories` - AI agent semantic memory
  - `stronghold_state` - Protected world infrastructure
- ✅ SQLAlchemy ORM with async support
- ✅ Alembic migration system
- ✅ FastAPI application with CORS
- ✅ Initial API endpoints:
  - `GET /health` - Health check
  - `POST /worlds/generate` - Create new world
  - `GET /worlds/{world_id}` - Retrieve world
  - `GET /worlds` - List worlds

### Database Features

- Enums for world types and government types
- JSON columns for flexible data storage (biomes, resources, relationships, etc.)
- Foreign key relationships with cascading deletes
- Indexes on frequently queried fields
- DateTime tracking for creation and updates

## API Usage

### Create a World

```bash
curl -X POST "http://localhost:8000/api/worlds/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "The Eternal Realm",
    "world_type": "normal",
    "generation_params": {
      "num_planets": 5,
      "num_civilizations": 10,
      "technology_level": 2.5,
      "world_seed": null
    }
  }'
```

### Retrieve World

```bash
curl "http://localhost:8000/api/worlds/{world_id}"
```

### List Worlds

```bash
curl "http://localhost:8000/api/worlds?skip=0&limit=10"
```

## Development Workflow

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=app  # With coverage
```

### Code Quality

```bash
# Format code
black app/

# Lint
ruff check app/

# Type checking
mypy app/
```

## Next Phases

### Phase 2: Multi-Agent AI System (Weeks 3-4)
- Agent base framework with tool calling
- Specialized agents (WorldArchitect, Civilization, StoryDirector, Guardian, Security)
- Memory system (short-term + long-term vector DB)
- Agent communication protocol

### Phase 3: World Generation Pipeline (Weeks 5-7)
- Terrain generation (Perlin noise, erosion simulation)
- Biome synthesis
- Civilization generation (governments, cultures, economies)
- City and location generation
- Procedural lore and history generation

### Phase 4: Simulation & Evolution (Weeks 8-9)
- Simulation tick system
- Civilization evolution (population, economy, politics)
- Dynamic event generation
- Background task scheduling

### Phase 5: Stronghold System (Weeks 10-11)
- Stronghold world type with protected districts
- Self-healing infrastructure
- Defense systems
- Backup and recovery

### Phase 6: Frontend Console (Weeks 12-13)
- React-based creator dashboard
- World visualization (3D viewer)
- Real-time monitoring
- Command interface

### Phase 7: Unreal Integration (Weeks 14-15)
- REST API for Unreal Engine
- Unreal plugin development
- Runtime world streaming
- Cinematic integration

### Phase 8: Security & Polish (Weeks 16-17)
- AI safety systems
- Performance optimization
- Scaling infrastructure
- Comprehensive testing

## Configuration

Edit `.env` to customize:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stronghold

# LLM (Phase 2)
LLM_PROVIDER=huggingface_local
LLM_MODEL=mistral-7b-instruct

# Simulation (Phase 4)
SIMULATION_TICK_INTERVAL=3600
MAX_CONCURRENT_WORLDS=10

# API
DEBUG=true
LOG_LEVEL=info
```

## Contributing

This is an active development project. Each phase builds on previous work:

1. Ensure Phase N foundation is solid before starting Phase N+1
2. Write tests for new functionality
3. Keep code modular and well-documented
4. Follow the implementation plan from `/root/.claude/plans/claude-code-task-auto-twinkling-glade.md`

## License

MIT

## Author

Shanee Baldwin

---

**Status**: Phase 1 ✅ Core Infrastructure Complete
**Next**: Phase 2 - Multi-Agent AI System