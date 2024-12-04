#!/bin/bash

# Set the container name or ID
CONTAINER_NAME="eadcf4876be9"
SERVICE_NAME="infinitech-website_fastapi"

# Pull the latest code from the main branch
echo "Pulling latest code from main branch..."
git pull origin main || { echo "Failed to pull latest code. Exiting."; exit 1; }

# Stop the specified container
echo "Stopping container $CONTAINER_NAME..."
docker stop "$CONTAINER_NAME" || { echo "Failed to stop container $CONTAINER_NAME. Exiting."; exit 1; }

# Remove the stopped container to avoid conflict
echo "Removing container $CONTAINER_NAME..."
docker rm "$CONTAINER_NAME" || { echo "Failed to remove container $CONTAINER_NAME. Exiting."; exit 1; }

# Prune unused Docker resources
echo "Pruning unused Docker resources..."
docker system prune -af --volumes || { echo "Failed to prune Docker system. Exiting."; exit 1; }

# Build and restart the container using docker-compose
echo "Building and starting new container..."
docker-compose up --build -d || { echo "Failed to build and start new container. Exiting."; exit 1; }

# Confirm the container is running
if docker ps | grep -q "$SERVICE_NAME"; then
    echo "Container $SERVICE_NAME is up and running."
else
    echo "Failed to start container $SERVICE_NAME. Check logs for details."
    exit 1
fi
