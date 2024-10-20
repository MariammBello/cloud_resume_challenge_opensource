#!/bin/bash

# Stop and remove old containers
echo "Stopping and removing old containers..."
docker compose down || true

# Pull latest images from GHCR
echo "Pulling latest images from GHCR..."
docker pull ghcr.io/mariammbello/resume-frontend:latest
docker pull ghcr.io/mariammbello/resume-backend:latest

# Start everything using Docker Compose
echo "Starting containers..."
docker compose up -d

echo "Update complete!"
 