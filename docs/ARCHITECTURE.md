# Architecture Guide

## System Overview

Shanee Intelligence Phase 1 MVP follows a classic three-tier architecture:

```
┌─────────────────────────────────────────────────────────┐
│                 Client Layer                             │
│         React 18 + TypeScript SPA (Vite)               │
│     (Home, Dashboard, SecureArea pages with auth)       │
└─────────────────────────────────────────────────────────┘
                          ↓ (HTTP/REST)
┌─────────────────────────────────────────────────────────┐
│                 API Gateway Layer                        │
│           FastAPI with JWT Authentication               │
│        (Auth, Status, User endpoints with CORS)         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│               Application Logic Layer                    │
│     Token validation, User management, Status reports   │
└─────────────────────────────────────────────────────────┘
```

## Frontend Architecture

### Component Structure
```
App.tsx (Router & Auth Guard)
├── Layout
│   ├── Navigation
│   ├── Page Outlet
│   └── Footer
├── pages/
│   ├── Home (Landing page)
│   ├── Dashboard (System status)
│   ├── SecureArea (Protected page)
│   └── Login (Authentication)
└── hooks/
    └── useAuth (Authentication state)
```

### Authentication Flow

1. **Login Page**: User enters credentials
2. **API Call**: `POST /api/auth/token` with username/password
3. **Token Storage**: JWT stored in localStorage
4. **State Management**: useAuth hook manages auth state
5. **Protected Routes**: ProtectedRoute component enforces authentication
6. **API Headers**: Bearer token sent with protected requests

### Styling Approach

- **Tailwind CSS**: Utility-first CSS framework
- **Dark Theme**: Dark background (gray-900) with cyan accents
- **Responsive Design**: Mobile-first approach with breakpoints
- **CSS-in-JS**: No, using pure CSS utilities via Tailwind
- **Component Variants**: Classes applied directly to elements

### Pages Overview

**Home Page**
- Landing page with project overview
- Three feature cards (Privacy, GPU, Distributed)
- Getting started guide
- No authentication required

**Dashboard Page**
- Real-time system status display
- Service health monitoring
- Auto-refreshing every 5 seconds
- 4-column metric cards
- Service status list with indicators

**SecureArea Page**
- Authenticated user information display
- User profile details
- Account creation date
- Secure features list
- Protected by JWT authentication

**Login Page**
- Simple authentication form
- Pre-filled demo credentials
- Error handling
- Loading state during request

## Backend Architecture

### API Structure

```
/
├── /auth
│   └── POST /token        - Get JWT access token
├── /status                - GET system status
├── /health                - GET health check
└── /api
    └── /user
        └── GET /me        - Get current user info
```

### Request/Response Flow

**Authentication Request**
```
POST /auth/token
Body: {"username": "admin", "password": "admin"}
Response: {"access_token": "jwt_token", "token_type": "bearer"}
```

**Protected Request**
```
GET /api/user/me
Headers: Authorization: Bearer {access_token}
Response: {"username": "admin", "role": "admin", "createdAt": "..."}
```

### Authentication Implementation

**Token Creation**
- Uses PyJWT library
- Secret key: "dev-secret-key-change-in-production"
- Algorithm: HS256
- Expiration: 30 minutes

**Token Validation**
- Extracted from Authorization header
- Decoded with same secret and algorithm
- Checked for expiration
- Returns 401 for invalid/expired tokens

### Error Handling

- **Invalid Credentials**: 401 Unauthorized
- **Missing Token**: 401 Unauthorized
- **Invalid Token**: 401 Unauthorized
- **Service Errors**: 500 Internal Server Error

## Data Models

### User Model
```typescript
{
  username: string
  role: string         // "admin" or "user"
  createdAt: string    // ISO 8601 timestamp
}
```

### Token Model
```typescript
{
  access_token: string
  token_type: string   // "bearer"
}
```

### SystemStatus Model
```typescript
{
  status: string       // "operational", etc.
  timestamp: string    // ISO 8601 timestamp
  version: string      // "0.1.0"
  services: {
    [key: string]: "running" | "stopped"
  }
}
```

## Infrastructure & Deployment

### Docker Compose Setup

**Services**:
1. **Frontend Service**
   - Image: Node 18 Alpine
   - Port: 5173
   - Volume: src/ for hot reload
   - Command: npm run dev

2. **Backend Service**
   - Image: Python 3.11 Slim
   - Port: 8000
   - Volume: app/ for auto-reload
   - Command: uvicorn main:app --reload
   - Health checks enabled

### Network Configuration

- CORS enabled for localhost:5173 and localhost:3000
- API proxy: `/api/*` → `http://localhost:8000`
- Services communicate via network name `shanee-network`

### Environment Variables

**Frontend (.env)**
```
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

**Backend (.env)**
```
FASTAPI_ENV=development
SECRET_KEY=dev-secret-key
DEBUG=True
```

## Security Considerations

### Current Implementation (Development)

⚠️ **Security Notes**:
- Hardcoded credentials (admin/admin)
- Plain text secret key
- No HTTPS in dev environment
- Tokens stored in localStorage (vulnerable to XSS)
- No rate limiting
- No request validation

### Production Improvements Needed

1. **Authentication**
   - Replace hardcoded credentials with database
   - Implement password hashing (bcrypt)
   - Add refresh tokens
   - Implement account lockout after failed attempts

2. **Transport Security**
   - Enable HTTPS/TLS
   - Implement HSTS headers
   - Use secure cookies instead of localStorage

3. **API Security**
   - Add rate limiting
   - Implement request signing
   - Add API key management
   - Validate all inputs

4. **Infrastructure**
   - Enable authentication on services
   - Use secrets management (e.g., AWS Secrets Manager)
   - Implement logging and monitoring
   - Add WAF protection

## Performance Optimization

### Frontend
- Code splitting via React Router
- Lazy loading for pages
- Asset minification via Vite
- Browser caching of static assets

### Backend
- Async/await for non-blocking I/O
- Connection pooling (future: database)
- Response caching for status endpoints
- Fast JSON serialization via Pydantic

### Scalability Path

**Phase 2+**:
- Add caching layer (Redis)
- Database for persistence (PostgreSQL)
- Message queue for async tasks (Celery/RabbitMQ)
- Load balancing across API servers
- CDN for static assets

## Testing Strategy

### Frontend
- Unit tests with Jest/Vitest
- Component tests with React Testing Library
- E2E tests with Cypress/Playwright
- Type checking with TypeScript strict mode

### Backend
- Unit tests with pytest
- Integration tests with TestClient
- API contract testing
- Load testing with locust

## Development Workflow

### Local Development
1. Start Docker Compose: `docker-compose up`
2. Frontend auto-updates on file changes (Vite)
3. Backend auto-reloads on file changes (Uvicorn)
4. Debug in browser DevTools
5. Use FastAPI Swagger UI at `/docs`

### Git Workflow
- Feature branches from main
- Pull requests for review
- Merge to main after approval
- Automated testing on PR

### Code Quality
- ESLint for JavaScript/TypeScript
- Prettier for code formatting
- Type checking with TypeScript
- Pylint/Black for Python

## Future Architecture Evolution

### Phase 2: Agent Management
- Add agent service
- Implement memory systems
- Tool registry and execution

### Phase 3: Distributed Systems
- P2P networking
- Distributed consensus
- Storage abstraction
- Simulation engine

### Phase 4: Enterprise Scale
- Kubernetes orchestration
- Multi-region deployment
- Enterprise authentication (SAML/OAuth2)
- Advanced monitoring and alerting
