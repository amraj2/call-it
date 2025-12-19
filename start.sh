#!/bin/bash

# Simple script to start Temporal server

echo "Starting Temporal server..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Start services
docker-compose up -d

echo ""
echo "Waiting for services to start..."
sleep 5

echo ""
echo "✅ Temporal server is starting!"
echo ""
echo "Services:"
docker-compose ps

echo ""
echo "🌐 Temporal UI: http://localhost:8088"
echo "🔌 Temporal Server: localhost:7233"
echo ""
echo "To stop: docker-compose down"

