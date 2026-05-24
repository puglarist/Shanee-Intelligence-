# Shanee Intelligence Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer (Browser)               │
│  ┌────────────────────────────────────────────────────┐ │
│  │  React SPA (TypeScript + Vite)                     │ │
│  │  - Authentication UI                               │ │
│  │  - Dashboard & Analytics                           │ │
│  │  - File Management Interface                       │ │
│  │  - Compute Job Submission                          │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                           ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────┐
│               API Layer (Backend)                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │  FastAPI (Python 3.11+)                            │ │
│  │  - Authentication & JWT                            │ │
│  │  - File Management API                             │ │
│  │  - Compute Job Orchestration                       │ │
│  │  - Status & Monitoring                             │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
           ↓              ↓              ↓
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ Database │  │ Storage  │  │GPU/Edge  │
    │(Future)  │  │(Multi)   │  │Compute   │
    └──────────┘  └──────────┘  └──────────┘
```

## Frontend Architecture

### Technology Stack
- **Framework**: React 18.2
- **Language**: TypeScript 5.2
- **Build Tool**: Vite 4.5
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **HTTP Client**: Fetch API (native)

### Directory Structure
```
frontend/
├── src/
│   ├── pages/           # Route components
│   │   ├── Home.tsx
│   │   ├── Dashboard.tsx
│   │   └── SecureArea.tsx
│   ├── components/      # Reusable components (future)
│   ├── hooks/          # Custom React hooks (future)
│   ├── services/       # API client services (future)
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── index.css       # Global styles
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

### Key Features
- **Responsive Design**: Works on iOS, tablets, and desktop
- **SPA Architecture**: Fast navigation without page reloads
- **API Integration**: Proxy setup for backend communication
- **Development**: Hot reload with Vite

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI 0.104
- **Python Version**: 3.11+
- **Server**: Uvicorn
- **Authentication**: JWT (PyJWT)
- **Configuration**: Pydantic Settings
- **Async**: Built-in with FastAPI

### Module Organization
```
backend/
├── main.py             # FastAPI application & routes
├── config.py           # Configuration management
├── pyproject.toml      # Poetry dependencies
├── .env.example        # Environment template
└── Dockerfile          # Container definition
```

### API Endpoints (MVP)
```
GET  /                  - API info
GET  /status            - System status
POST /auth/token        - Authentication
GET  /api/user/me       - Current user
POST /api/files/upload  - File upload (stub)
POST /api/compute/submit - GPU job (stub)
```

### Authentication Flow
```
1. Client sends username/password to POST /auth/token
2. Backend validates credentials
3. Backend returns JWT access token
4. Client stores token in memory/localStorage
5. Client includes token in Authorization header
6. Backend validates token on protected endpoints
```

## Data Flow

### Authentication Sequence
```
Browser                                    Backend
  │                                           │
  ├─── POST /auth/token ────────────────────>│
  │     {username, password}                  │
  │                                           │
  │<───── 200 OK ──────────────────────────────┤
  │     {access_token, token_type}             │
  │                                           │
  └─ Store token in memory ─────────┐         │
                                    │         │
  ┌─── GET /api/user/me ────────────┼────────>│
  │ Header: Authorization: Bearer {token}    │
  │                                 │         │
  │<─────── 200 OK ─────────────────┘─────────┤
  │     {username, ...}                       │
```

## Infrastructure

### Docker Compose Services (Development)
- **frontend**: React dev server (port 5173)
- **backend**: FastAPI dev server (port 8000)
- **postgres**: PostgreSQL (port 5432, commented out)

### Network Configuration
- Internal Docker network: `shanee-network`
- Frontend proxy: Requests to `/api/*` forwarded to backend:8000
- CORS enabled for local development (http://localhost:5173, 3000)

## Security Architecture (MVP Foundation)

### Current Implementation
- JWT token-based authentication
- CORS middleware for API access control
- Environment-based configuration

### Phase 2 Plan
- Proper credential management
- Encrypted file storage
- Rate limiting & request throttling
- Input validation & sanitization
- HTTPS enforcement
- Secure token refresh mechanism

### Phase 3 Plan
- End-to-end encryption
- Zero-knowledge architecture
- Audit logging
- Compliance tracking

## Scalability Considerations

### Horizontal Scaling (Phase 2+)
- Stateless backend (no session state)
- JWT allows load balancing
- Database abstraction ready
- API versioning in place

### GPU Integration (Phase 2+)
- Runpod API abstraction layer
- Job queue system
- Async job processing
- Result webhooks/polling

## Development Workflow

### Local Development
```bash
# Start all services
docker-compose up

# Or run individually
npm run dev        # Frontend
poetry run uvicorn main:app --reload  # Backend
```

### API Testing
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Postman/curl for custom requests

## Deployment Strategy

### Production Build
1. Build frontend: `npm run build` → `/dist` folder
2. Serve frontend from CDN or static server
3. Run backend with production Dockerfile
4. Set environment variables properly
5. Enable HTTPS and proper CORS

### Container Strategy
- Separate containers for frontend (Node.js) and backend (Python)
- Frontend can be served via Nginx/Apache
- Backend runs with Gunicorn/Uvicorn in production
- Database (PostgreSQL) optional until Phase 2

## Future Enhancements

### Phase 2
- Database integration (PostgreSQL)
- File encryption implementation
- GitHub API integration
- Cloud storage backends (S3, CloudKit)
- Runpod GPU integration
- Advanced monitoring & logging

### Phase 3
- Omniverse UI with WebGL
- IPFS decentralized storage
- Edge device orchestration
- AI/ML experiment sandbox
- Advanced security features

---

**Last Updated**: Phase 1 MVP
**Status**: Architecture finalized for Phase 1, ready for Phase 2 expansion
