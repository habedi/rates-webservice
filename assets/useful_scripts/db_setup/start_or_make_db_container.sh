#!/bin/bash

# Loading the environment variables
source .env

# Create the data directory if it does not exist
if [ ! -d "$DOCKER_DATA_DIR" ]; then
    echo "Creating the data directory $DOCKER_DATA_DIR"
    mkdir -p "$DOCKER_DATA_DIR"
fi

# Docker needs a full path!
data_dir_full_path=$(readlink -f "$DOCKER_DATA_DIR")

# Create the container if it does not exist
if [ "$(docker ps -a | grep "$DOCKER_CONTAINER")" ]; then
    echo "Container $DOCKER_CONTAINER already exists"
else
    echo "Creating container $DOCKER_CONTAINER"
    docker create --name "$DOCKER_CONTAINER" -p "$DB_PORT":"$DOCKER_PORT" \
    -v "$data_dir_full_path:/var/lib/postgresql/data" "$DOCKER_IMAGE"
fi

echo "Starting the $DOCKER_CONTAINER Docker container"
docker start "$DOCKER_CONTAINER"

echo "Checking the running Docker containers:"
docker ps
