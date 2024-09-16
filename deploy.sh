#!/bin/bash

echo "Stopping and removing old frontend containers..."
docker stop frontend
docker rm frontend

# Pull the latest images from GitHub Container Registry
echo "Pulling latest frontend images from GHCR..."
docker pull ghcr.io/your-gh-username/resume-frontend:latest


# Run the Frontend container
echo "Starting Frontend container..."
docker run -d --name frontend -p 80:80 ghcr.io/your-gh-username/resume-frontend:latest

echo "Update complete!"