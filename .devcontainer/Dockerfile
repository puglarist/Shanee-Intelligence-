# Multi-stage build for Omniverse Engine
# Stage 1: Base development environment
FROM node:20-bullseye as base

# Set environment variables
ENV NODE_ENV=development \
    DEBUG=omniverse:* \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    sqlite3 \
    libsqlite3-dev \
    python3 \
    python3-pip \
    curl \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Stage 2: Development environment with node modules
FROM base as development

# Copy package files
COPY backend/package.json backend/package-lock.json* ./backend/

# Install dependencies
RUN cd backend && npm ci --prefer-offline --no-audit

# Copy entire project
COPY . .

# Create data directory for SQLite
RUN mkdir -p /workspace/data /media/external

# Expose ports
EXPOSE 3000 3001 8080

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 --start-period=30s \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["npm", "run", "dev"]
