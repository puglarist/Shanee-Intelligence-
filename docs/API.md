# Portable Omniverse Engine - API Reference

## Server Configuration

- **Base URL**: `http://localhost:3000`
- **WebSocket**: `ws://localhost:3000/ws/updates`
- **Content-Type**: `application/json`

## Authentication

Currently no authentication. Future versions will support:
- API keys
- JWT tokens
- OAuth 2.0

## Health & Status

### GET /health

Check server health status.

**Response** (200 OK):
```json
{
  "status": "ok",
  "ok": true,
  "timestamp": "2026-05-29T12:00:00.000Z",
  "database": "/workspace/data/omniverse.db"
}
```

---

## World Management

### GET /api/world/states

List all world states.

**Response** (200 OK):
```json
[
  {
    "name": "default",
    "data": {
      "name": "Default World",
      "description": "...",
      "earthEnabled": true,
      "spaceEnabled": true
    },
    "created_at": "2026-05-29T10:00:00Z",
    "updated_at": "2026-05-29T12:00:00Z"
  }
]
```

### GET /api/world/:name

Get specific world state.

**Parameters**:
- `name` (string, required) - World name

**Response** (200 OK):
```json
{
  "name": "default",
  "description": "Default Omniverse world",
  "earthEnabled": true,
  "spaceEnabled": true,
  "time": 12345.6,
  "paused": false
}
```

**Response** (404 Not Found):
```json
{
  "error": "World not found"
}
```

### POST /api/world/create

Create new world.

**Request Body**:
```json
{
  "name": "my-world",
  "description": "Custom world",
  "earthEnabled": true,
  "spaceEnabled": true
}
```

**Response** (201 Created):
```json
{
  "name": "my-world",
  "created": true,
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### POST /api/world/:name/reset

Reset world to initial state.

**Response** (200 OK):
```json
{
  "name": "default",
  "reset": true,
  "timestamp": "2026-05-29T12:00:00Z"
}
```

---

## Simulation Control

### POST /api/sim/start

Start simulation.

**Request Body** (optional):
```json
{
  "world": "default",
  "speed": 1.0
}
```

**Response** (200 OK):
```json
{
  "status": "running",
  "speed": 1.0,
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### POST /api/sim/pause

Pause simulation.

**Response** (200 OK):
```json
{
  "status": "paused",
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### POST /api/sim/reset

Reset simulation.

**Response** (200 OK):
```json
{
  "status": "reset",
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### GET /api/sim/state

Get current simulation state.

**Response** (200 OK):
```json
{
  "running": true,
  "time": 12345.6,
  "speed": 1.0,
  "earth": {
    "timeOfDay": 14.5,
    "weather": {
      "windSpeed": 5.2,
      "temperature": 18,
      "humidity": 65
    }
  },
  "space": {
    "bodies": [
      {
        "name": "Earth",
        "position": {"x": 1.496e11, "y": 0, "z": 0},
        "velocity": {"x": 0, "y": 29780, "z": 0}
      }
    ]
  },
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### POST /api/sim/setSpeed

Set simulation speed.

**Request Body**:
```json
{
  "speed": 100.0
}
```

**Response** (200 OK):
```json
{
  "speed": 100.0,
  "timestamp": "2026-05-29T12:00:00Z"
}
```

---

## Asset Management

### GET /api/assets/list

List available assets.

**Query Parameters**:
- `type` (string, optional) - Filter by type (earth, space, terrain)

**Response** (200 OK):
```json
{
  "assets": [
    {
      "name": "earth_texture_4k",
      "type": "earth",
      "size": 52428800,
      "hash": "sha256:abc123...",
      "registered": "2026-05-29T10:00:00Z"
    }
  ]
}
```

### GET /api/assets/:name

Stream asset.

**Parameters**:
- `name` (string, required) - Asset name

**Response** (200 OK):
- Content: Binary asset data
- Headers:
  - `Content-Type: application/octet-stream`
  - `Content-Length: <bytes>`
  - `X-Asset-Hash: <sha256>`
  - `X-Asset-Size: <bytes>`

### GET /api/assets/:name/metadata

Get asset metadata.

**Response** (200 OK):
```json
{
  "name": "earth_texture_4k",
  "type": "earth",
  "size": 52428800,
  "hash": "sha256:abc123...",
  "exists": true,
  "cached": false,
  "registered": "2026-05-29T10:00:00Z"
}
```

### POST /api/assets/register

Register new asset.

**Request Body**:
```json
{
  "name": "terrain_001",
  "type": "earth",
  "path": "/media/external/omniverse/earth/terrain_001"
}
```

**Response** (201 Created):
```json
{
  "name": "terrain_001",
  "type": "earth",
  "registered": true,
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### POST /api/assets/:name/cache

Cache asset locally.

**Response** (200 OK):
```json
{
  "name": "terrain_001",
  "cached": true,
  "path": "/workspace/data/cache/terrain_001",
  "timestamp": "2026-05-29T12:00:00Z"
}
```

---

## Synchronization

### GET /api/sync/status

Get sync status.

**Response** (200 OK):
```json
{
  "syncing": false,
  "lastSync": "2026-05-29T11:30:00Z",
  "queueSize": 5,
  "conflicts": 0,
  "cloudConnected": true
}
```

### POST /api/sync/push

Sync local changes to cloud.

**Response** (202 Accepted):
```json
{
  "syncing": true,
  "jobId": "sync-job-123",
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### POST /api/sync/pull

Sync from cloud to local.

**Response** (202 Accepted):
```json
{
  "syncing": true,
  "jobId": "sync-job-124",
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### GET /api/sync/history

Get sync history.

**Query Parameters**:
- `limit` (number, optional, default 50)
- `offset` (number, optional, default 0)

**Response** (200 OK):
```json
{
  "entries": [
    {
      "id": "sync-entry-1",
      "action": "push",
      "entityType": "world",
      "entityId": "default",
      "localVersion": 1,
      "remoteVersion": 0,
      "conflict": false,
      "timestamp": "2026-05-29T12:00:00Z"
    }
  ],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

---

## Bluetooth Management

### GET /api/bluetooth/devices

List paired Bluetooth devices.

**Response** (200 OK):
```json
{
  "devices": [
    {
      "uuid": "...",
      "name": "iPhone 14",
      "macAddress": "...",
      "paired": true,
      "lastSeen": "2026-05-29T12:00:00Z"
    }
  ]
}
```

### POST /api/bluetooth/pair

Initiate device pairing.

**Request Body**:
```json
{
  "deviceUuid": "..."
}
```

**Response** (200 OK):
```json
{
  "deviceUuid": "...",
  "pairing": true,
  "timeout": 30000
}
```

### POST /api/bluetooth/unpair

Unpair device.

**Request Body**:
```json
{
  "deviceUuid": "..."
}
```

**Response** (200 OK):
```json
{
  "deviceUuid": "...",
  "unpaired": true
}
```

### POST /api/bluetooth/command

Send command to device.

**Request Body**:
```json
{
  "deviceUuid": "...",
  "command": "PLAY",
  "payload": {"speed": 1}
}
```

**Response** (202 Accepted):
```json
{
  "commandId": "cmd-123",
  "status": "queued",
  "timestamp": "2026-05-29T12:00:00Z"
}
```

---

## WebSocket API

### Connection

```javascript
const ws = new WebSocket('ws://localhost:3000/ws/updates');
```

### Messages

**Subscribe to updates**:
```json
{
  "type": "subscribe",
  "clientId": "client-123",
  "subscriptions": ["world", "simulation", "assets"]
}
```

**Send command**:
```json
{
  "type": "command",
  "command": "PAUSE",
  "payload": {},
  "id": "cmd-456"
}
```

**Response**:
```json
{
  "type": "command_queued",
  "id": "cmd-456"
}
```

**Receive update** (broadcast):
```json
{
  "type": "world_updated",
  "world": {...},
  "timestamp": "2026-05-29T12:00:00Z"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Invalid request body",
  "details": {...}
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Internal server error",
  "requestId": "req-123"
}
```

---

## Rate Limiting

Currently unlimited. Future versions will implement:
- 100 requests/minute per IP
- 1000 requests/minute per API key
- WebSocket connection limits

---

## Pagination

Endpoints supporting pagination use:
- `limit` (default 50, max 500)
- `offset` (default 0)

Response includes:
```json
{
  "data": [...],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 142
  }
}
```

---

## Timestamps

All timestamps are ISO 8601 format (UTC):
```
2026-05-29T12:00:00.000Z
```

---

## Code Examples

### JavaScript/Node.js

```javascript
// Fetch world state
const response = await fetch('http://localhost:3000/api/world/default');
const world = await response.json();
console.log(world);

// Send command via WebSocket
const ws = new WebSocket('ws://localhost:3000/ws/updates');
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'command',
    command: 'PLAY',
    payload: { speed: 1 }
  }));
};
```

### Python

```python
import requests
import websocket

# REST API
response = requests.get('http://localhost:3000/api/sim/state')
state = response.json()

# WebSocket
def on_message(ws, msg):
    print(f"Received: {msg}")

ws = websocket.WebSocketApp('ws://localhost:3000/ws/updates')
ws.on_message = on_message
ws.run_forever()
```

### Swift/iOS

```swift
// Use BluetoothManager from ios/BluetoothManager.swift
let manager = BluetoothManager()
manager.sendCommand("PLAY")
```

---

For more information, see `ARCHITECTURE.md` and `README.md`.
