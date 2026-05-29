#!/bin/bash

set -e

echo "=== Omniverse Engine Bootstrap ==="
echo "Initializing development environment..."

# Create necessary directories
mkdir -p data
mkdir -p media/external
mkdir -p logs

# Navigate to backend
cd backend

# Install dependencies
echo "Installing dependencies..."
npm ci

# Run database migrations
echo "Running database migrations..."
node db/migrate.js

# Initialize test data
echo "Seeding database with initial data..."
node db/seed.js

# Run health check
echo "Running health checks..."
npm run health-check || true

echo ""
echo "=== Bootstrap Complete ==="
echo "Backend running on http://localhost:3000"
echo "Health check available at http://localhost:3000/health"
echo ""
echo "To start development:"
echo "  cd backend && npm run dev"
echo ""
