#!/bin/bash
# Enter test Postgres container and open psql directly

# Find the test Postgres container
CONTAINER_NAME=$(docker ps --filter "name=fastapi_test_postgres" --format "{{.Names}}")

if [ -z "$CONTAINER_NAME" ]; then
    echo "Test Postgres container not running."
    exit 1
fi

echo "Entering Test Postgres container: $CONTAINER_NAME"
# Run psql directly inside the container
docker exec -it $CONTAINER_NAME psql -U test_user -d test_db
