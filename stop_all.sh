#!/bin/bash

# Script to stop all Temporal services

set -e

# Detect Python command (for consistency)
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🛑 Stopping all services..."
echo ""

# Stop worker if PID file exists
if [ -f .worker.pid ]; then
    WORKER_PID=$(cat .worker.pid)
    if ps -p $WORKER_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping worker (PID: $WORKER_PID)...${NC}"
        kill $WORKER_PID 2>/dev/null || true
        sleep 1
        # Force kill if still running
        kill -9 $WORKER_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Worker stopped.${NC}"
    fi
    rm .worker.pid
fi

# Stop Flask if PID file exists
if [ -f .flask.pid ]; then
    FLASK_PID=$(cat .flask.pid)
    if ps -p $FLASK_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping Flask app (PID: $FLASK_PID)...${NC}"
        kill $FLASK_PID 2>/dev/null || true
        sleep 1
        # Force kill if still running
        kill -9 $FLASK_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Flask app stopped.${NC}"
    fi
    rm .flask.pid
fi

# Stop Docker containers
echo -e "${YELLOW}Stopping Temporal server...${NC}"
docker-compose down
echo -e "${GREEN}✅ Temporal server stopped.${NC}"

echo ""
echo -e "${GREEN}✅ All services stopped successfully!${NC}"

