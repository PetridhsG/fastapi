#!/bin/bash
# Enter Postgres container and open psql directly

# Find the Postgres container
CONTAINER_NAME=$(docker ps --filter "name=fastapi_postgres" --format "{{.Names}}")

if [ -z "$CONTAINER_NAME" ]; then
    echo "Postgres container not running."
    exit 1
fi

echo "Entering Postgres container: $CONTAINER_NAME"
# Run psql directly inside the container
docker exec -it $CONTAINER_NAME psql -U postgres -d fastapi
