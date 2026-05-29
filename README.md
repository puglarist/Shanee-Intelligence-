# Shanee Intelligence

An AI-assisted cinematic omniverse development ecosystem combining distributed intelligence, procedural world generation, persistent simulations, and spatial computing.

## Ecosystem Overview

Shanee Intelligence is an umbrella research initiative and infrastructure foundation supporting:

- **AI Orchestration**: Advanced agent coordination, memory systems, and tool ecosystems
- **Distributed Systems**: Privacy-first, GPU-accelerated multi-agent infrastructure
- **Omniverse Engine**: Cinematic simulation platform with procedural world generation
- **Stronghold Initiative**: Protected persistent worlds with AI governance systems
- **Spatial Computing**: iOS/Swift integration with Vision Pro support
- **Creator Ecosystems**: Tools and infrastructure for building within the omniverse

## Divisions

### Shanee Intelligence (Core)
The parent organization providing:
- AI orchestration framework
- Research umbrella
- Infrastructure foundation
- Long-term ecosystem architecture

### Omniverse Engine
The cinematic simulation platform featuring:
- Unreal Engine 5 runtime systems
- AI-generated procedural worlds
- Cinematic rendering and visualization
- Multiplayer sandbox infrastructure
- Simulation and civilization systems

### Stronghold System
The persistent universe protection layer:
- Protected persistent worlds
- AI governance infrastructure
- Creator command centers
- Simulation recovery architecture

### iOS + Swift Layer
Portable omniverse terminals:
- SwiftUI dashboard
- Spatial computing interface
- Vision Pro ecosystem
- Mobile orchestration

## Phase 1: MVP

The Phase 1 MVP establishes the foundational full-stack application with:
- **Frontend**: React 18 + TypeScript + Vite with responsive dark-theme UI
- **Backend**: FastAPI with JWT authentication and REST API
- **Infrastructure**: Docker Compose orchestration for local development
- **Documentation**: Comprehensive setup and architecture guides

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker Compose

```bash
docker-compose up
```

This starts:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Local Development

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Default Credentials

**Username**: `admin`  
**Password**: `admin`

⚠️ These are for MVP development only. Change them for production deployment.

## Project Structure

```
shanee-intelligence/
├── frontend/                 # React SPA with Vite
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components (Home, Dashboard, SecureArea)
│   │   ├── hooks/           # Custom React hooks
│   │   ├── App.tsx          # Main app with routing
│   │   └── main.tsx         # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── backend/                 # FastAPI server
│   ├── main.py             # FastAPI application
│   ├── pyproject.toml
│   └── Dockerfile
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md
│   └── API.md
├── docker-compose.yml      # Container orchestration
└── .gitignore
```

## Features

### Frontend
- **Multi-page Navigation**: Home (landing), Dashboard (system status), SecureArea (authenticated)
- **Responsive Design**: Mobile-first Tailwind CSS with dark theme
- **Authentication**: JWT-based login with local storage
- **Real-time Updates**: Live system status polling
- **Hot Reload**: Vite dev server with instant feedback

### Backend
- **REST API**: Organized endpoints with clear structure
- **Authentication**: JWT token generation and validation
- **CORS Support**: Pre-configured for local development
- **Health Checks**: System status and service monitoring
- **Async Support**: FastAPI async/await for scalability

## API Endpoints

### Authentication
- `POST /auth/token` - Get JWT access token

### Public
- `GET /status` - System status and service health
- `GET /health` - Health check

### Protected (Requires Bearer Token)
- `GET /api/user/me` - Get current user information

## Documentation

See detailed documentation:
- [Architecture Guide](docs/ARCHITECTURE.md) - System design and components
- [API Documentation](docs/API.md) - Complete endpoint reference

## Development Workflow

### Making Changes

1. **Frontend Changes**
   ```bash
   cd frontend
   # Edit src/ files
   npm run type-check
   npm run build
   ```

2. **Backend Changes**
   ```bash
   cd backend
   # Edit main.py
   # Changes auto-reload with uvicorn --reload
   ```

### Building for Production

```bash
# Frontend
cd frontend
npm run build
# Output in frontend/dist/

# Backend
cd backend
# Build and push Docker image
docker build -t shanee-intelligence-backend:latest .
```

## Deployment

### Docker Deployment

```bash
docker-compose -f docker-compose.yml up -d
```

### Environment Configuration

Copy environment templates and configure:
```bash
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
```

## Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **React Router v6** - Client-side routing
- **Tailwind CSS** - Utility-first styling
- **Vite** - Build tool

### Backend
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **PyJWT** - Authentication
- **Uvicorn** - ASGI server

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Node.js** - Frontend runtime
- **Python 3.11** - Backend runtime

## Repository Structure

This monorepo contains the complete Shanee Intelligence ecosystem:

```
shanee-intelligence/
├── apps/                      # Deployable applications
│   ├── backend/               # Core API and orchestration
│   ├── omniverse-engine/      # Unreal Engine runtime
│   ├── stronghold/            # Persistent world systems
│   ├── ios-swift/             # Mobile interfaces
│   └── creator-console/       # Creator tools
├── engine/                    # Core simulation engines
│   ├── unreal-engine/         # UE5 integration
│   ├── simulation-runtime/    # Simulation infrastructure
│   ├── world-generation/      # Procedural generation
│   ├── multiplayer/           # Networking and sync
│   ├── cinematics/            # Rendering and visualization
│   └── ai-orchestration/      # Agent coordination
├── infrastructure/            # Cloud and deployment
│   ├── docker/
│   ├── kubernetes/
│   ├── cloud/
│   └── portable-storage/
├── ai-systems/                # Intelligence layers
│   ├── agents/                # Agent implementations
│   ├── llm-orchestration/     # Language model coordination
│   ├── memory-systems/        # Memory management
│   └── civilization-ai/       # Civilization engines
└── repo-tasks/                # Development task ecosystem
    ├── milestones/
    ├── epics/
    ├── features/
    ├── bugs/
    ├── research/
    ├── ai-systems/
    ├── simulation-systems/
    ├── unreal-engine/
    ├── ios-swift/
    ├── backend/
    ├── security/
    ├── multiplayer/
    ├── cinematics/
    ├── procedural-worlds/
    ├── stronghold/
    ├── performance/
    └── deployment/
```

## Task Management System

This repository uses an integrated task orchestration system to manage all development across the ecosystem. Tasks are organized by:

- **Milestones**: Major project phases and releases
- **Epics**: Large feature initiatives
- **Features**: Concrete development tasks
- **Research**: R&D and exploration tasks
- **Domain-Specific Tasks**: Organized by system (Unreal Engine, AI, iOS, Security, etc.)

See `repo-tasks/` directory for the task ecosystem and development roadmap.

## Development Phases

**Phase 1**: MVP Foundation (Current)
- Core API and authentication
- Frontend dashboard
- Docker infrastructure
- Task orchestration system

**Phase 2**: Agent & Memory Systems
- Multi-agent orchestration
- Advanced memory management (episodic, semantic, procedural)
- Tool ecosystem and registry
- API route organization

**Phase 3**: Omniverse Engine Foundation
- Unreal Engine 5 integration
- Plugin architecture
- World streaming systems
- Cinematic rendering pipeline

**Phase 4**: AI World Generation
- Hugging Face orchestration
- Procedural terrain generation
- AI NPC systems
- Civilization generation

**Phase 5**: Stronghold Implementation
- Persistent world systems
- AI governance infrastructure
- Secure save systems
- Recovery architecture

**Phase 6**: Multiplayer Infrastructure
- Dedicated server setup
- Matchmaking systems
- Voice communication
- World synchronization

**Phase 7**: iOS + Swift Integration
- SwiftUI dashboard
- Unreal Engine bridge
- Bluetooth discovery
- Vision Pro support

**Phase 8**: Optimization & Scaling
- GPU optimization
- Streaming optimization
- AI compute balancing
- Planetary simulation scale

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Contact

For questions or support, visit the project repository or contact the development team.
