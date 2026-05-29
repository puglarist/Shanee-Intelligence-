# Shanee Intelligence

A privacy-focused GPU-accelerated platform for distributed AI orchestration and multi-agent systems.

## Project Overview

Shanee Intelligence is a complete platform designed to enable:
- **Privacy-First Architecture**: End-to-end encryption and local processing
- **GPU Acceleration**: High-performance compute workloads and AI inference
- **Distributed Systems**: Multi-agent orchestration across multiple nodes
- **Scalable Infrastructure**: Cloud-native deployment and horizontal scaling

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

## Next Phases

**Phase 2**: Core agent, memory, and tool management systems
- Multi-agent orchestration
- Advanced memory management
- Tool ecosystem and registry

**Phase 3**: Omniverse OS platform
- Distributed networking
- Simulation engine
- Complete cloud infrastructure

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Contact

For questions or support, visit the project repository or contact the development team.
