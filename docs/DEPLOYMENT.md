# Portable Omniverse Engine - Deployment Guide

## Deployment Environments

This guide covers deployment to various environments.

## 1. GitHub Codespaces (Cloud Development)

### Quickest Setup

1. Fork/Clone repo to GitHub
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for container to build (~5 minutes)
4. Terminal automatically opens in `/workspace`

### After Container Ready

```bash
# Install backend dependencies
cd backend
npm ci

# Initialize database
npm run db:migrate
npm run db:seed

# Start development server
npm run dev
```

Access at: `http://localhost:3000` (Codespaces will prompt to open)

### Advantages
- ✓ No local setup required
- ✓ Pre-configured environment
- ✓ Auto port forwarding
- ✓ Browser-based VS Code
- ✓ Linux environment with all tools

### Cost
- Free: 120 core-hours/month
- Paid: $0.18/core-hour

### Troubleshooting
```bash
# Rebuild container
Dev Containers: Rebuild Container (Cmd+Shift+P)

# Check logs
View → Output → DevContainers

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm ci
```

---

## 2. Docker Compose (Local Development)

### Prerequisites
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- Docker Compose 2.0+
- 4GB RAM minimum
- 2GB disk space

### Setup

```bash
# Clone repository
git clone https://github.com/puglarist/Shanee-Intelligence-.git
cd Shanee-Intelligence-

# Build and start services
docker-compose up

# In another terminal, bootstrap
npm run bootstrap
```

### Access
- Backend API: `http://localhost:3000`
- Simulator: `http://localhost:3001`
- Health check: `http://localhost:8080/health`

### Development Workflow

```bash
# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Clean everything
docker-compose down -v

# Rebuild image
docker-compose build --no-cache
```

### Database Access

```bash
# Connect to SQLite
docker exec -it $(docker-compose ps -q backend) sqlite3 /workspace/data/omniverse.db

# Run migrations
docker exec $(docker-compose ps -q backend) npm run db:migrate
```

---

## 3. External Drive Deployment

### Prerequisites
- External SSD/HDD (USB 3.0+ recommended)
- 1GB minimum space
- Linux/macOS/Windows system

### Setup Steps

#### Step 1: Prepare External Drive

```bash
# Linux/macOS
sudo mkdir -p /media/external/omniverse
sudo chown -R $(whoami) /media/external/omniverse

# Or for /mnt/
sudo mkdir -p /mnt/omniverse
sudo mount /dev/sdX1 /mnt/omniverse
```

#### Step 2: Copy Project

```bash
# Clone to external drive
git clone https://github.com/puglarist/Shanee-Intelligence-.git /media/external/omniverse

# Or copy existing installation
cp -r ./Shanee-Intelligence- /media/external/omniverse/
```

#### Step 3: Install Node.js on Drive

```bash
cd /media/external/omniverse
# Use Node.js portable version or system-installed Node
```

#### Step 4: Initialize Database

```bash
export DATABASE_URL=/media/external/omniverse/data/omniverse.db
export EXTERNAL_DRIVE_PATH=/media/external/omniverse

cd backend
npm ci
npm run db:migrate
npm run db:seed
```

#### Step 5: Run

```bash
npm run dev
```

### Configuration

Create `.env` on external drive:

```bash
# Copy template
cp .env.example .env

# Edit for external drive
nano .env
# Set: EXTERNAL_DRIVE_PATH=/media/external/omniverse
# Set: DATABASE_URL=/media/external/omniverse/data/omniverse.db
```

### Cross-Platform Portability

The engine auto-detects external drives:

```javascript
// Automatic detection on startup:
// Linux: /proc/mounts → /media, /mnt
// macOS: /Volumes
// Windows: C-Z drive letters
```

### Usage Scenarios

#### Home Network Streaming
```
Laptop A (Server)
  ↓ Network
Laptop B (Client) → http://laptop-a-ip:3000

iPhone (Bluetooth) ↔ Laptop A
```

#### Offline Field Work
```
External Drive (on USB SSD)
  ↓
Laptop (no internet)
  ↓
iPhone (Bluetooth via local network)
```

#### Hot Swap Between Devices
```
Device A → Eject drive
  ↓
Insert drive to Device B
  ↓
Run same data/simulation
```

---

## 4. iOS App Deployment

### Development Setup

#### Prerequisites
- Mac with Xcode 15+
- iOS 14+ target device
- Apple Developer Account (free for testing)

#### Steps

1. Open `ios/OmniverseRemote.swift` in Xcode
2. Select target device/simulator
3. Build: Cmd+B
4. Run: Cmd+R

#### Testing on Simulator

```bash
# Start Xcode simulator
open -a Simulator

# Check available devices
xcrun simctl list devices

# Record app interactions
xcrun simctl io booted recordVideo simulation.mp4
```

### Production Distribution

#### App Store
```bash
# 1. Create App ID in Apple Developer
# 2. Create provisioning profile
# 3. Build for distribution
xcodebuild -scheme OmniverseRemote -archivePath OmniverseRemote.xcarchive -configuration Release archive

# 4. Submit to App Store
# (Through Xcode Organizer or Transporter)
```

#### TestFlight
```bash
# Internal testing via TestFlight
# 1. Archive app (Xcode)
# 2. Submit to TestFlight
# 3. Invite testers via App Store Connect
```

#### Manual Installation
```bash
# For development/testing:
# 1. Archive app
# 2. Export as Ad Hoc provisioned IPA
# 3. Install via Xcode to physical device
xcodebuild -scheme OmniverseRemote -configuration Release \
  -exportPath . -exportOptionsPlist ExportOptions.plist
```

---

## 5. Production Deployment

### Server Infrastructure

#### VPS Options
- DigitalOcean App Platform
- Heroku (if free tier available)
- AWS EC2
- Google Cloud Run
- Azure Container Instances

#### Recommended: Digital Ocean

```bash
# 1. Create App on App Platform
# 2. Connect GitHub repository
# 3. Configure:
PORT=3000
DATABASE_URL=/data/omniverse.db
EXTERNAL_DRIVE_PATH=/mnt/storage

# 4. Deploy
# Automatic on git push
```

### Database Backup

```bash
# Automated backup
0 2 * * * cp /data/omniverse.db /backups/omniverse.db.$(date +\%Y\%m\%d)

# Restore
cp /backups/omniverse.db.20260529 /data/omniverse.db
```

### Monitoring

#### Health Checks
```bash
# Kubernetes liveness probe
curl http://localhost:3000/health

# Continuous monitoring
watch -n 5 'curl -s http://localhost:3000/health'
```

#### Logging

```bash
# Centralized logging (future)
DEBUG=omniverse:* node server.js 2>&1 | \
  tee -a /var/log/omniverse.log | \
  logstash-shipper
```

### Scaling

#### Horizontal Scaling
- Run multiple backend instances
- Load balancer (nginx/HAProxy)
- Shared database (PostgreSQL)
- Shared asset storage (S3/GCS)

#### Example nginx config
```nginx
upstream omniverse {
    server localhost:3000;
    server localhost:3001;
}

server {
    listen 80;
    server_name omniverse.example.com;
    
    location / {
        proxy_pass http://omniverse;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 6. Troubleshooting Deployment

### Container Issues

```bash
# Debug container
docker run -it --rm -v $(pwd):/app node:20 bash

# Check Docker version
docker --version
docker-compose --version

# Reset Docker
docker system prune -a
```

### Database Issues

```bash
# Check database integrity
sqlite3 /data/omniverse.db "PRAGMA integrity_check;"

# Recover from corruption
sqlite3 /data/omniverse.db ".dump" > dump.sql
rm /data/omniverse.db
sqlite3 /data/omniverse.db < dump.sql
```

### Network Issues

```bash
# Check ports
lsof -i :3000
lsof -i :3001
lsof -i :8080

# Firewall
sudo ufw allow 3000/tcp
sudo ufw allow 3001/tcp
```

### Bluetooth Issues (iOS)

```bash
# Check Bluetooth capability
system_profiler SPBluetoothDataType

# Reset Bluetooth
sudo killall -9 bluetoothd
```

---

## 7. Performance Optimization

### Backend
```bash
# Enable clustering
NODE_ENV=production node --cluster server.js

# Use compression
npm install compression
# In server.js: app.use(compression());
```

### Database
```bash
# Optimize queries
PRAGMA analyze;
PRAGMA optimize;

# Increase cache
PRAGMA cache_size = 10000;
```

### Assets
```bash
# Pre-compress assets
gzip -9 -r assets/
# Configure nginx for gzip on-the-fly
```

---

## Summary Table

| Environment | Setup Time | Cost | Best For |
|-------------|-----------|------|----------|
| Codespaces | 5 min | Free (120h/mo) | Development |
| Docker | 10 min | Free | Local testing |
| External Drive | 15 min | Drive cost | Portable offline |
| VPS | 30 min | $5-20/mo | Production |
| Kubernetes | 1 hour | Variable | Enterprise |

---

For more help, see README.md and ARCHITECTURE.md
