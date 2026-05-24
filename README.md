# Shanee Intelligence

A privacy-focused, GPU-accelerated web platform designed as a secure "stronghold" for computational intelligence operations.

## Vision

Shanee Intelligence is a multi-layered platform combining secure computing, GPU acceleration, and decentralized storage to create a comprehensive environment for intelligence gathering, data analysis, and AI/ML experimentation—all with security and privacy as foundational principles.

### Core Features (Planned)
- **Security**: End-to-end encryption, secure compute isolation, authentication/authorization
- **GPU Acceleration**: Integration with Runpod GPUs and edge devices (Orange Pi) for AI/ML workloads
- **Decentralized Storage**: Multi-backend support (GitHub, cloud storage, IPFS)
- **Omniverse Interface**: Immersive, multi-environment UI
- **iOS-Friendly**: Responsive web design for mobile and desktop

## Architecture

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **Target**: iOS-friendly responsive web app

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Authentication**: JWT tokens
- **Database**: PostgreSQL (optional, for future use)
- **API Documentation**: Auto-generated OpenAPI/Swagger

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **GPU Compute**: Runpod integration (planned)
- **Storage**: Multi-backend (local, S3, GitHub)
- **Deployment**: Docker, with scaling options (Kubernetes-ready)

## Development Setup

### Prerequisites
- Docker & Docker Compose (recommended)
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Poetry (Python dependency management)

### Quick Start with Docker Compose

```bash
# Clone and navigate to project
cd Shanee-Intelligence

# Start all services
docker-compose up

# Frontend will be available at http://localhost:5173
# Backend API at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Local Development (Without Docker)

#### Backend Setup
```bash
cd backend

# Install dependencies
poetry install

# Set up environment
cp .env.example .env

# Run the server
poetry run uvicorn main:app --reload

# API docs at http://localhost:8000/docs
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Open http://localhost:5173
```

## API Endpoints

### Authentication
- `POST /auth/token` - Get access token
  - Default credentials (MVP): `username: admin`, `password: admin`

### System
- `GET /` - API info
- `GET /status` - System status (GPU, storage, etc.)
- `GET /api/user/me` - Current user info (requires auth)

### Files (Planned)
- `POST /api/files/upload` - Upload encrypted file
- `GET /api/files` - List files
- `DELETE /api/files/{id}` - Delete file

### Compute (Planned)
- `POST /api/compute/submit` - Submit GPU job
- `GET /api/compute/jobs` - List compute jobs
- `GET /api/compute/jobs/{id}` - Job status

## Project Structure

```
Shanee-Intelligence/
├── frontend/                    # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/              # Page components
│   │   ├── App.tsx             # Main app component
│   │   ├── main.tsx            # Entry point
│   │   └── index.css           # Styles
│   ├── index.html              # HTML template
│   ├── vite.config.ts          # Vite configuration
│   ├── tsconfig.json           # TypeScript config
│   ├── package.json            # NPM dependencies
│   └── Dockerfile              # Frontend container
│
├── backend/                     # Python + FastAPI backend
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── pyproject.toml          # Poetry dependencies
│   ├── .env.example            # Environment template
│   └── Dockerfile              # Backend container
│
├── infrastructure/              # Deployment & infra configs
│   └── (coming soon)
│
├── docs/                        # Documentation
│   └── (coming soon)
│
├── docker-compose.yml          # Local development orchestration
└── README.md                   # This file
```

## Development Phases

### Phase 1: MVP (Current)
- ✅ Basic project scaffolding
- ✅ React frontend with routing
- ✅ FastAPI backend with auth
- ✅ Docker Compose setup
- ⏳ Test core connectivity

### Phase 2: Core Features
- [ ] Secure user authentication & session management
- [ ] File upload/download with encryption
- [ ] GitHub integration (read/write repos)
- [ ] Cloud storage support (S3, iOS CloudKit)
- [ ] GPU compute job submission (Runpod)
- [ ] Dashboard with compute status

### Phase 3: Advanced Features
- [ ] Omniverse/immersive UI (WebGL/Babylon.js)
- [ ] Decentralized storage (IPFS)
- [ ] Edge compute orchestration
- [ ] AI/ML experiment sandbox
- [ ] Security audit logging

## Configuration

### Environment Variables

Backend (`backend/.env`):
```
SECRET_KEY=your-secret-key
DEBUG=true
RUNPOD_API_KEY=optional-runpod-key
STORAGE_BACKEND=local  # or s3, github
GITHUB_TOKEN=optional-github-token
```

Frontend (`frontend/.env.local`):
```
VITE_API_URL=http://localhost:8000
```

## Testing

### Backend
```bash
cd backend
poetry run pytest
```

### Frontend
```bash
cd frontend
npm run test  # (coming soon)
```

## Deployment

### Production Build
```bash
# Frontend
cd frontend
npm run build

# Backend with production Dockerfile
docker build -t shanee-backend:latest ./backend
```

### Docker Compose for Production
(Configuration coming in Phase 2)

## Security Considerations

- **Default Credentials**: The MVP uses hardcoded credentials (`admin/admin`). Replace with proper authentication.
- **Secret Key**: Change `SECRET_KEY` in production.
- **CORS**: Update `CORS_ORIGINS` in `backend/main.py` for production domains.
- **Encryption**: File encryption and end-to-end encryption implementations coming in Phase 2.

## Contributing

1. Create a feature branch from `claude/clever-lovelace-ASzE5`
2. Make changes following code patterns established in Phase 1
3. Test locally with Docker Compose
4. Commit with clear messages
5. Push and create a pull request

## Open Questions

- **Authentication**: GitHub OAuth or custom JWT?
- **GPU Workloads**: What compute tasks will dominate?
- **Encryption**: End-to-end or server-side initially?
- **Deployment**: AWS, DigitalOcean, self-hosted, hybrid?

## License

TBD

## Contact

For questions or collaboration inquiries, contact the Shanee Intelligence team.

---

**Phase 1 Status**: Scaffold complete. Ready for Phase 2 feature development.