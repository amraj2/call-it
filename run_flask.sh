#!/bin/bash

# Script to run the Flask app

echo "🌐 Starting Flask app..."
echo ""

# Check if Temporal server is running
if ! nc -z localhost 7233 2>/dev/null; then
    echo "⚠️  Warning: Temporal server is not running on localhost:7233"
    echo "   The Flask app will start, but workflows won't work until the server is running."
    echo ""
fi

# Check if worker is running (optional check)
echo "💡 Make sure the Temporal worker is running in another terminal:"
echo "   ./run_worker.sh"
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

# Run Flask app
export FLASK_PORT=${FLASK_PORT:-8000}
$PYTHON_CMD app.py

