# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses Bearer token authentication via JWT. Include the token in the Authorization header:

```
Authorization: Bearer {access_token}
```

## Endpoints

### Authentication

#### Get Access Token

**Request**
```
POST /auth/token
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Response (200 OK)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized)**
```json
{
  "detail": "Invalid credentials"
}
```

**Notes**:
- Token expires after 30 minutes
- Username must be "admin" for MVP
- Use the access_token with Bearer authentication for protected endpoints
- Token type is always "bearer"

---

### System Status

#### Get System Status

**Request**
```
GET /status
```

**Response (200 OK)**
```json
{
  "status": "operational",
  "timestamp": "2024-05-29T10:30:45.123456",
  "version": "0.1.0",
  "services": {
    "authentication": "running",
    "api": "running",
    "database": "running"
  }
}
```

**Notes**:
- No authentication required
- Returns real-time system status
- Services object contains status of each service
- Possible service statuses: "running", "stopped", "degraded"

---

### Health Check

#### Health Check Endpoint

**Request**
```
GET /health
```

**Response (200 OK)**
```json
{
  "status": "healthy"
}
```

**Notes**:
- No authentication required
- Used for load balancer health checks
- Returns 200 if service is running

---

### User Management

#### Get Current User Info

**Request**
```
GET /api/user/me
Authorization: Bearer {access_token}
```

**Response (200 OK)**
```json
{
  "username": "admin",
  "role": "admin",
  "createdAt": "2024-05-29T10:00:00.000000"
}
```

**Error Response (401 Unauthorized)**
```json
{
  "detail": "Invalid token"
}
```

**Notes**:
- Requires valid JWT access token
- Token must be in Authorization header as Bearer token
- Returns current authenticated user's information
- Role is "admin" for admin user, "user" for others

---

## Error Responses

### Common Error Codes

**400 Bad Request**
```json
{
  "detail": "Invalid request body"
}
```

**401 Unauthorized**
```json
{
  "detail": "Invalid credentials"
}
```
```json
{
  "detail": "No authorization header"
}
```
```json
{
  "detail": "Invalid token"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

---

## Usage Examples

### JavaScript/Fetch

**Login and Get Token**
```javascript
const response = await fetch('http://localhost:8000/auth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin'
  })
});

const data = await response.json();
const token = data.access_token;
```

**Fetch Protected Endpoint**
```javascript
const response = await fetch('http://localhost:8000/api/user/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const user = await response.json();
console.log(user);
```

**Check System Status**
```javascript
const response = await fetch('http://localhost:8000/status');
const status = await response.json();
console.log(`System Status: ${status.status}`);
```

### Python/Requests

**Login and Get Token**
```python
import requests

response = requests.post('http://localhost:8000/auth/token', json={
    'username': 'admin',
    'password': 'admin'
})

data = response.json()
token = data['access_token']
```

**Fetch Protected Endpoint**
```python
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/user/me', headers=headers)
user = response.json()
print(user)
```

### cURL

**Login**
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

**Fetch Protected Endpoint**
```bash
TOKEN="your_access_token_here"
curl -X GET http://localhost:8000/api/user/me \
  -H "Authorization: Bearer $TOKEN"
```

**Check Status**
```bash
curl http://localhost:8000/status
```

---

## Rate Limiting

Currently not implemented in MVP. Future versions will include:
- Per-IP rate limiting
- Per-user rate limiting
- Endpoint-specific limits

---

## CORS Policy

Allowed origins:
- `http://localhost:5173` (Frontend dev server)
- `http://localhost:3000` (Alternative dev port)

Methods: GET, POST, PUT, DELETE, OPTIONS
Headers: All

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Use these interfaces to explore and test endpoints directly.

---

## Response Headers

All responses include standard HTTP headers:

```
Content-Type: application/json
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Credentials: true
```

---

## Data Types

### String
- ISO 8601 timestamps: `"2024-05-29T10:30:45.123456"`
- Bearer tokens: `"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`

### Number
- Integers for counts and IDs
- Floats for metrics and percentages

### Object
- Flat JSON objects for simplicity
- Arrays for lists of items

---

## Versioning

Current API version: **0.1.0**

Version is included in system status responses. Future versions will include `/v1/`, `/v2/` prefixes for compatibility.

---

## Webhook Support

Not currently implemented. Future versions will support:
- Event subscriptions
- Real-time WebSocket connections
- Server-sent events (SSE)

---

## Pagination

Not currently needed for MVP responses. Future versions will include:
- Limit/offset pagination
- Cursor-based pagination
- Page size defaults

---

## Filtering and Sorting

Currently not supported. Will be added as data volume increases.

---

## Batch Operations

Not currently supported. Single endpoint calls required for each operation.

---

## File Upload/Download

Placeholder endpoints exist for future implementation:
- File upload for agent artifacts
- Log file download
- Report generation

---

## WebSocket Support

Not currently implemented. Planned for:
- Real-time agent status updates
- Live log streaming
- Agent-to-agent communication

---

## Support

For API issues or questions:
1. Check interactive docs at `/docs`
2. Review this reference
3. Check project README and ARCHITECTURE guides
4. Open an issue on GitHub

---

## Changelog

### Version 0.1.0 (Current)
- Initial MVP API
- Authentication endpoint
- Status and health checks
- User information endpoint
- CORS middleware
- JWT token validation
