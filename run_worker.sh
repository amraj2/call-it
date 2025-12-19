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

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found. Please install Python 3."
    exit 1
fi

# Run the worker
$PYTHON_CMD temporal_worker.py

