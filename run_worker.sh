#!/bin/bash

# Script to run the Temporal worker

echo "🚀 Starting Temporal worker..."
echo ""

# Check if Temporal server is running
if ! nc -z localhost 7233 2>/dev/null; then
    echo "❌ Error: Temporal server is not running on localhost:7233"
    echo "   Please start it first with: docker-compose up -d"
    exit 1
fi

echo "✅ Temporal server is accessible"
echo ""

# Run the worker
python temporal_worker.py

