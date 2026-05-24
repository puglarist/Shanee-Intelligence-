# Shanee Intelligence Omniverse OS

A unified, polyglot intelligence operating system that spans multiple paradigms: centralized AI orchestration, distributed P2P networks, local-first edge computing, and immersive simulated environments.

## Vision

The Omniverse OS is a meta-system that adapts its architecture, execution model, and interfaces to serve diverse use cases while maintaining semantic coherence across all domains. It's built on the philosophy of being:

- **Omnipresent**: Available as monolithic service, microservices, serverless functions, or P2P nodes
- **Omniscient**: Unified knowledge graphs across siloed systems, multi-modal understanding
- **Omniarchitectural**: Works across Python, TypeScript, Go, Rust without friction
- **Omniverse**: Supports AI, distributed systems, simulation, and metaverse applications

## Quick Start

### Prerequisites
- Python 3.11+
- Poetry for dependency management
- Claude API key (for AI features)

### Installation

```bash
# Clone the repository
git clone https://github.com/puglarist/shanee-intelligence-
cd shanee-intelligence-

# Install dependencies
pip install poetry
poetry install

# Set up environment
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Running the REPL

```bash
poetry run shanee repl
```

This starts an interactive command-line interface where you can:
- Create agents
- Manage conversations
- Test the intelligence core

### Starting the API Server

```bash
poetry run shanee server
```

The server will start on `http://localhost:8000`. Access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

The system is organized into 7 core layers:

1. **Intelligence Core** - AI/ML capabilities with Claude API integration
2. **Agent Runtime** - Stateful multi-agent coordination
3. **Execution Engine** - Task scheduling and async workflows
4. **Distribution Layer** - P2P networking and consensus (coming soon)
5. **Storage Substrate** - Distributed ledger and knowledge graphs (coming soon)
6. **Simulation Engine** - Virtual environments and metaverse (coming soon)
7. **Interface Layer** - REST APIs, CLI, Web UI, mobile apps

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## Project Structure

```
shanee-intelligence-omniverse/
├── docs/                    # Architecture and protocol docs
├── core/                    # Core platform
│   ├── intelligence/        # AI/ML core
│   ├── agent/               # Agent runtime
│   ├── tools/               # Tool registry
│   └── memory/              # Memory systems
├── sdk/                     # Client SDKs (Python, TypeScript, Go, Rust)
├── network/                 # Distributed networking
├── simulation/              # Simulation engine
├── services/                # Microservices
│   └── orchestrator/        # Main API server
├── ui/                      # User interfaces
├── examples/                # Reference implementations
└── tests/                   # Test suites
```

## Key Features

### For AI Developers
- ✅ Unified agent framework with multi-model support
- ✅ Sophisticated tool ecosystem with schemas
- ✅ Conversation memory and context management
- ✅ Easy integration with Claude APIs

### For Systems Engineers
- 🔄 Microservices-ready architecture
- 🔄 P2P networking foundation (in progress)
- 🔄 Distributed storage integration (in progress)
- 🔄 Kubernetes deployment support (coming)

### For Researchers
- 🔄 Configurable simulation environments (coming)
- 🔄 Multi-agent research framework (coming)
- 🔄 Emergent behavior analysis tools (coming)

### For End Users
- ✅ Intuitive conversational interface
- ✅ Agent management dashboard (coming)
- 🔄 Privacy-preserving local-first mode (coming)

## API Examples

### Create an Agent

```bash
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "description": "My first agent",
    "model_id": "claude-opus-4-7"
  }'
```

### Send a Message

```bash
curl -X POST http://localhost:8000/agents/{agent_id}/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you do?"}'
```

### List Agents

```bash
curl http://localhost:8000/agents
```

## Protocol Specification

The system uses a universal message envelope for all communication:

```json
{
  "id": "uuid-string",
  "timestamp": "2026-05-24T13:30:00Z",
  "version": "1.0",
  "type": "agent.request|agent.response|tool.call|event",
  "source": "agent-id|service-id",
  "payload": {}
}
```

See [PROTOCOL.md](docs/PROTOCOL.md) for complete specification.

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Quality

```bash
# Format code
poetry run black .

# Lint
poetry run ruff check .

# Type check
poetry run mypy core
```

### Building Documentation

```bash
# View architecture diagrams and docs
open docs/ARCHITECTURE.md
```

## Roadmap

### Phase 1: Foundation (MVP) ✅
- [x] Core protocol and message formats
- [x] Python SDK with Claude API integration
- [x] Basic agent runtime
- [x] REST API server
- [x] Simple CLI interface

### Phase 2: Intelligence (In Progress)
- [ ] Multi-agent orchestration
- [ ] Advanced memory systems
- [ ] Extended tool ecosystem
- [ ] Web dashboard

### Phase 3: Distribution
- [ ] P2P networking layer
- [ ] Consensus mechanisms
- [ ] Distributed storage
- [ ] Horizontal scaling

### Phase 4: Simulation & Metaverse
- [ ] Virtual environment engine
- [ ] Agent embodiment
- [ ] Physics simulation
- [ ] Emergent behavior

### Phase 5: Advanced Features
- [ ] Federated learning
- [ ] Cryptographic identity
- [ ] Autonomous value creation
- [ ] External blockchain integration

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please follow the architecture guidelines in [CLAUDE.md](CLAUDE.md) and ensure all tests pass.

## Documentation

- [CLAUDE.md](CLAUDE.md) - Project overview and development guidelines
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [docs/PROTOCOL.md](docs/PROTOCOL.md) - Protocol specification
- [docs/API.md](docs/API.md) - API reference (coming soon)

## Support

For questions or issues:
- 📧 Email: baldwinshane09@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/puglarist/shanee-intelligence-/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/puglarist/shanee-intelligence-/discussions)

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built with:
- [Anthropic Claude](https://claude.ai) - AI backbone
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [SQLAlchemy](https://sqlalchemy.org/) - Database ORM
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

**Shanee Intelligence Omniverse OS** - Unified intelligence across all domains
