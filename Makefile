.PHONY: help setup init-dev install test lint format typecheck run-repl run-server run-dev clean docs

help:
	@echo "Shanee Intelligence Omniverse OS - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup              Install dependencies and prepare environment"
	@echo "  make init-dev           Initialize development environment"
	@echo ""
	@echo "Development:"
	@echo "  make run-repl          Start interactive REPL"
	@echo "  make run-server        Start API server"
	@echo "  make run-dev           Start development server with auto-reload"
	@echo ""
	@echo "Code Quality:"
	@echo "  make test              Run all tests"
	@echo "  make lint              Run linters"
	@echo "  make format            Format code"
	@echo "  make typecheck         Run type checking"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean             Remove build artifacts"
	@echo "  make docs              Build documentation"

setup:
	pip install poetry
	poetry install
	pre-commit install

init-dev:
	cp .env.example .env || true
	poetry run alembic upgrade head || true
	@echo "✅ Development environment initialized"

install:
	poetry install

test:
	poetry run pytest --cov=core --cov=shanee

lint:
	poetry run ruff check .
	poetry run pylint core shanee || true

format:
	poetry run black .
	poetry run ruff check --fix .

typecheck:
	poetry run mypy core shanee

run-repl:
	poetry run shanee repl

run-server:
	poetry run shanee server

run-dev:
	poetry run shanee dev

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf build dist *.egg-info

docs:
	@echo "📚 Documentation available in docs/"
	@echo "- ARCHITECTURE.md - System architecture"
	@echo "- PROTOCOL.md - Protocol specification"
	@echo "- API.md - API reference (coming soon)"

# Development tasks
.PHONY: dev-watch dev-test dev-lint

dev-watch:
	poetry run pytest --cov=core --cov=shanee -v --tb=short

dev-test:
	poetry run pytest -v --tb=short

dev-lint:
	poetry run ruff check --watch .

# Docker commands
.PHONY: docker-build docker-run docker-stop

docker-build:
	docker build -t shanee-intelligence:latest .

docker-run:
	docker run -p 8000:8000 -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} shanee-intelligence:latest

docker-stop:
	docker stop shanee-intelligence || true
	docker rm shanee-intelligence || true

# Kubernetes commands
.PHONY: k8s-deploy k8s-delete k8s-logs

k8s-deploy:
	kubectl apply -f kubernetes/

k8s-delete:
	kubectl delete -f kubernetes/

k8s-logs:
	kubectl logs -f deployment/shanee-orchestrator

# CI/CD
.PHONY: ci-check ci-test ci-build

ci-check:
	@echo "Running CI checks..."
	@$(MAKE) typecheck
	@$(MAKE) lint
	@$(MAKE) test

ci-test:
	poetry run pytest --cov=core --cov=shanee --cov-report=xml

ci-build:
	poetry build
