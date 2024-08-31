#!/bin/bash

# Loading the environment variables
source ".env"

echo "Stopping and removing the $DOCKER_CONTAINER Docker container..."
docker stop "$DOCKER_CONTAINER"
docker rm -f "$DOCKER_CONTAINER"

echo "Might need root privileges to remove the data directory..."
sudo rm -rf "$DOCKER_DATA_DIR"

echo "Removing the $DOCKER_IMAGE Docker image..."
docker rmi -f "$DOCKER_IMAGE"

echo "Docker image, container, and the data deleted successfully!"