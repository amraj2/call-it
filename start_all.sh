#!/bin/bash

# Script to start Temporal server, worker, and Flask app

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Starting Temporal Server, Worker, and Flask App..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Docker is not running.${NC}"
    echo "   Please start Docker Desktop and try again."
    exit 1
fi

# Step 1: Start Temporal server
echo -e "${GREEN}Step 1:${NC} Starting Temporal server..."
docker-compose up -d

# Wait for Temporal server to be ready
echo ""
echo "⏳ Waiting for Temporal server to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if nc -z localhost 7233 2>/dev/null; then
        echo -e "${GREEN}✅ Temporal server is ready!${NC}"
        break
    fi
    attempt=$((attempt + 1))
    echo "   Attempt $attempt/$max_attempts..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}❌ Error: Temporal server did not start in time.${NC}"
    echo "   Check logs with: docker logs temporal"
    exit 1
fi

# Give it a few more seconds to fully initialize
sleep 3

# Detect Python command and virtual environment
if [ -d "venv" ] && [ -f "venv/bin/python3" ]; then
    PYTHON_CMD="venv/bin/python3"
    echo "   Using virtual environment: venv/bin/python3"
elif [ -d "venv" ] && [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
    echo "   Using virtual environment: venv/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "   Using system Python: python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "   Using system Python: python"
else
    echo -e "${RED}❌ Error: Python not found.${NC}"
    echo "   Please install Python 3 and try again."
    exit 1
fi

# Check if temporalio is installed
if ! $PYTHON_CMD -c "import temporalio" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Warning: temporalio module not found.${NC}"
    echo "   Installing dependencies..."
    $PYTHON_CMD -m pip install -q -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error: Failed to install dependencies.${NC}"
        exit 1
    fi
fi

# Step 2: Start the worker in background
echo ""
echo -e "${GREEN}Step 2:${NC} Starting Temporal worker..."
$PYTHON_CMD temporal_worker.py > worker.log 2>&1 &
WORKER_PID=$!

# Check if worker started successfully
sleep 2
if ! ps -p $WORKER_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Worker failed to start.${NC}"
    echo "   Check logs: cat worker.log"
    echo ""
    if grep -q "ModuleNotFoundError" worker.log 2>/dev/null; then
        echo "   Issue: Missing Python dependencies"
        echo "   Fix: pip install -r requirements.txt"
    fi
    exit 1
fi

echo "   Worker started (PID: $WORKER_PID)"
echo "   Logs: worker.log"

# Wait a moment for worker to initialize
sleep 2

# Step 3: Start Flask app in background
echo ""
echo -e "${GREEN}Step 3:${NC} Starting Flask app..."

# Check if port 8000 is already in use
if lsof -ti:8000 > /dev/null 2>&1; then
    echo -e "${YELLOW}   ⚠️  Port 8000 is already in use.${NC}"
    echo "   Attempting to free the port..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 3
    # Verify port is free
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo -e "${RED}   ❌ Could not free port 8000.${NC}"
        echo "   Please manually stop the process using: lsof -ti:8000 | xargs kill"
        kill $WORKER_PID 2>/dev/null || true
        exit 1
    fi
fi

$PYTHON_CMD app.py > flask.log 2>&1 &
FLASK_PID=$!

# Check if Flask started successfully
sleep 3
if ! ps -p $FLASK_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Flask app failed to start.${NC}"
    echo "   Check logs: cat flask.log"
    echo ""
    echo "   Common issues:"
    echo "   - Port 8000 is in use: lsof -ti:8000 | xargs kill"
    echo "   - Python dependencies missing: pip install -r requirements.txt"
    # Try to kill worker if Flask failed
    kill $WORKER_PID 2>/dev/null || true
    exit 1
fi

echo "   Flask app started (PID: $FLASK_PID)"
echo "   Logs: flask.log"

# Wait for Flask to be ready
echo "   Waiting for Flask to be ready..."
max_attempts=10
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if nc -z localhost 8000 2>/dev/null; then
        echo -e "${GREEN}   ✅ Flask app is ready!${NC}"
        break
    fi
    attempt=$((attempt + 1))
    sleep 1
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${YELLOW}   ⚠️  Warning: Flask app may not be ready yet.${NC}"
    echo "   Check logs: tail -f flask.log"
fi

# Save PIDs to a file for easy cleanup
echo "$WORKER_PID" > .worker.pid
echo "$FLASK_PID" > .flask.pid

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Services:"
echo "  🌐 Flask App:     http://localhost:8000"
echo "  🔌 Temporal UI:  http://localhost:8088"
echo "  📊 Temporal API: localhost:7233"
echo ""
echo "Process IDs:"
echo "  Worker PID: $WORKER_PID"
echo "  Flask PID:  $FLASK_PID"
echo ""
echo "Logs:"
echo "  Worker: tail -f worker.log"
echo "  Flask:  tail -f flask.log"
echo ""
echo "To stop all services:"
echo "  ./stop_all.sh"
echo "  (or: docker-compose down && kill $WORKER_PID $FLASK_PID)"
echo ""
echo "Press Ctrl+C to stop this script (services will continue)"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    if [ -f .worker.pid ]; then
        kill $(cat .worker.pid) 2>/dev/null || true
        rm .worker.pid
    fi
    if [ -f .flask.pid ]; then
        kill $(cat .flask.pid) 2>/dev/null || true
        rm .flask.pid
    fi
    docker-compose down
    echo -e "${GREEN}✅ All services stopped.${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Keep script running
echo "Services are running. Press Ctrl+C to stop all services..."
while true; do
    sleep 1
done

