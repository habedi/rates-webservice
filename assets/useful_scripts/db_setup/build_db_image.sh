#!/bin/bash

# Loading the environment variables
source ".env"

echo "Building the $DOCKER_IMAGE Docker image..."
docker build \
  --build-arg DB_NAME="$DB_NAME" \
  --build-arg DB_USER="$DB_USER" \
  --build-arg DB_PASSWORD="$DB_PASSWORD" \
  --build-arg DB_HOST="$DB_HOST" \
  --build-arg DB_PORT="$DB_PORT" \
  -t "$DOCKER_IMAGE" -f "$DOCKERFILE" "$DOCKER_BUILD_CONTEXT"

echo "Checking the available Docker images:"
docker images