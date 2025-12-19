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
echo "   python temporal_worker.py"
echo ""

# Run Flask app
export FLASK_PORT=${FLASK_PORT:-5001}
python app.py

