#!/bin/bash

# Loading the environment variables
source .env

echo "Stopping the $DOCKER_CONTAINER Docker container..."
docker stop "$DOCKER_CONTAINER"

echo "Checking the available Docker containers:"
docker ps -a