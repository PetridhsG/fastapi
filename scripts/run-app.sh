#!/bin/bash
# Starts all Docker Compose containers
echo "Starting all containers..."
docker-compose up -d
echo "Containers started."
docker ps
