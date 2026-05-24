# Shanee Protocol Specification v1.0

## Message Format

All messages follow this envelope structure:

```json
{
  "id": "uuid-string",
  "timestamp": "2026-05-24T13:30:00Z",
  "version": "1.0",
  "type": "agent.request|agent.response|tool.call|tool.result|event|heartbeat",
  "source": "agent-id|service-id|node-id",
  "destination": "agent-id|service-id|*",
  "payload": {},
  "headers": {
    "priority": "high|normal|low",
    "idempotency_key": "uuid-string",
    "trace_id": "uuid-string",
    "span_id": "uuid-string"
  },
  "metadata": {}
}
```

## Message Types

### Agent Request
```json
{
  "type": "agent.request",
  "payload": {
    "agent_id": "string",
    "action": "string",
    "parameters": {},
    "context": {
      "session_id": "string",
      "conversation_id": "string",
      "user_id": "string"
    }
  }
}
```

### Agent Response
```json
{
  "type": "agent.response",
  "payload": {
    "agent_id": "string",
    "result": {},
    "status": "success|failure|pending",
    "error": null | {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
}
```

### Tool Call
```json
{
  "type": "tool.call",
  "payload": {
    "tool_id": "string",
    "tool_version": "string",
    "arguments": {},
    "metadata": {
      "timeout_ms": 30000,
      "retries": 3
    }
  }
}
```

### Tool Result
```json
{
  "type": "tool.result",
  "payload": {
    "tool_id": "string",
    "result": {},
    "execution_time_ms": 123,
    "status": "success|failure"
  }
}
```

### Event
```json
{
  "type": "event",
  "payload": {
    "event_type": "string",
    "entity_id": "string",
    "data": {},
    "timestamp": "2026-05-24T13:30:00Z"
  }
}
```

## Agent Interface

### Core Methods
```python
class Agent:
    async def perceive(self, input: Input) -> Perception
    async def think(self, perception: Perception) -> Decision
    async def act(self, decision: Decision) -> Action
    async def remember(self, experience: Experience) -> None
```

### Tool Schema
```json
{
  "id": "tool.read_file",
  "version": "1.0",
  "name": "read_file",
  "description": "Read contents of a file",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "File path to read"
      }
    },
    "required": ["path"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "content": {"type": "string"},
      "size_bytes": {"type": "integer"}
    }
  }
}
```

## Knowledge Graph Format

Semantic triples following RDF standard:
```
subject predicate object

Example:
agent:alice type Agent
agent:alice hasCapability tool:send_email
agent:alice hasMemory:episode episode:001
```

## Storage Format

### Event Log (Append-Only)
```
timestamp,event_type,entity_id,data_hash,data_json
2026-05-24T13:30:00Z,agent.created,alice,hash123,{...}
2026-05-24T13:30:01Z,tool.executed,read_file,hash124,{...}
```

### Object Store (Content-Addressed)
```
hash(content) → binary_data
ipfs://QmXxxx... → file_contents
```

## Network Protocol

### P2P Message Exchange
1. Peer discovery via DHT with `/shanee/1.0.0` protocol
2. Message signing with Ed25519 keys
3. Symmetric encryption (ChaCha20-Poly1305) for payloads
4. Keep-alive heartbeats every 30 seconds

### Service-to-Service (gRPC)
- Protocol Buffers for schema definition
- Mutual TLS for authentication
- Deadline propagation for timeouts

## Versioning & Compatibility

- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Breaking Changes**: Increment MAJOR version
- **New Features**: Increment MINOR version
- **Bug Fixes**: Increment PATCH version

Servers MUST support protocol versions within ±1 MAJOR version.

## Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| 1000 | Success | Operation completed successfully |
| 2000 | BadRequest | Invalid input parameters |
| 2001 | Unauthorized | Authentication required |
| 2002 | Forbidden | Permission denied |
| 3000 | InternalError | Server-side error |
| 3001 | Timeout | Operation exceeded timeout |
| 3002 | ResourceExhausted | Rate limit or quota exceeded |
| 4000 | NotFound | Resource not found |
| 5000 | Unavailable | Service temporarily unavailable |

## Consensus Protocol (Raft)

- **Term**: Monotonic counter for leadership election
- **Log Index**: Position in transaction log
- **Committed Index**: Last applied state machine entry

Follows standard Raft specification with 5-second election timeout.
