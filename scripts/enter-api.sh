#!/bin/bash
# Enter FastAPI container
CONTAINER_NAME=$(docker ps --filter "name=fastapi-project-api" --format "{{.Names}}")
if [ -z "$CONTAINER_NAME" ]; then
    echo "FastAPI container not running."
    exit 1
fi
echo "Entering FastAPI container: $CONTAINER_NAME"
docker exec -it $CONTAINER_NAME bash
