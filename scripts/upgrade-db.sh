#!/bin/bash
# run_migrations.sh
# Enter API container, ensure Alembic is installed, and run migrations

CONTAINER_NAME="fastapi-project-api-1"

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container ${CONTAINER_NAME} is not running."
    exit 1
fi

echo "Entering container ${CONTAINER_NAME}..."

docker exec -it $CONTAINER_NAME bash -c "
    source /app/.venv/bin/activate && \
    if ! pip show alembic > /dev/null 2>&1; then
        echo 'Alembic not found. Installing...'
        pip install alembic
    fi && \
    echo 'Running Alembic migrations...' && \
    alembic upgrade head
"
