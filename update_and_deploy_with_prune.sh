#!/bin/bash

# Set the Docker service name
SERVICE_NAME="infinitech-website_fastapi"

# Pull the latest code from the main branch
echo "Pulling latest code from main branch..."
git pull origin main || { echo "Failed to pull latest code. Exiting."; exit 1; }

# Find the container ID for the service
CONTAINER_ID=$(docker ps -qf "name=$SERVICE_NAME")

if [ -n "$CONTAINER_ID" ]; then
    # Stop the running container
    echo "Stopping container $CONTAINER_ID for service $SERVICE_NAME..."
    docker stop "$CONTAINER_ID" || { echo "Failed to stop container $CONTAINER_ID. Exiting."; exit 1; }

    # Remove the stopped container
    echo "Removing container $CONTAINER_ID..."
    docker rm "$CONTAINER_ID" || { echo "Failed to remove container $CONTAINER_ID. Exiting."; exit 1; }
else
    echo "No running container found for service $SERVICE_NAME. Proceeding with build."
fi

# Prune unused Docker resources
echo "Pruning unused Docker resources..."
docker system prune -af --volumes || { echo "Failed to prune Docker system. Exiting."; exit 1; }

# Build and restart the container using docker-compose
echo "Building and starting new container for service $SERVICE_NAME..."
docker-compose up --build -d || { echo "Failed to build and start new container. Exiting."; exit 1; }

# Confirm the container is running
if docker ps | grep -q "$SERVICE_NAME"; then
    echo "Container for service $SERVICE_NAME is up and running."
else
    echo "Failed to start container for service $SERVICE_NAME. Check logs for details."
    exit 1
fi
