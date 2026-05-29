#!/bin/bash

# Stronghold Genesis AI - Setup Script

set -e

echo "🚀 Setting up Stronghold Genesis AI Development Environment"

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file - please configure if needed"
fi

# Start Docker containers
echo "🐳 Starting Docker containers..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt || pip install poetry && poetry install

# Run database migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

echo ""
echo "✨ Setup complete! You can now start the API:"
echo "  python -m uvicorn app.main:app --reload"
echo ""
echo "📚 API documentation: http://localhost:8000/docs"
