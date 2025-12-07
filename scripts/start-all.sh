#!/bin/bash
# Run this from project root: ./scripts/start-all.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   ML-Powered AI News Platform - Quick Start       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running in the correct directory
if [ ! -d "genai-with-agentic-ai" ] || [ ! -d "Backend" ] || [ ! -d "Frontend" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# Check and kill processes on required ports
echo -e "${YELLOW}Checking for running services...${NC}"

if check_port 8000; then
    echo -e "${YELLOW}Port 8000 is in use. Stopping existing GenAI service...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

if check_port 5000; then
    echo -e "${YELLOW}Port 5000 is in use. Stopping existing Backend service...${NC}"
    lsof -ti:5000 | xargs kill -9 2>/dev/null
fi

if check_port 5173; then
    echo -e "${YELLOW}Port 5173 is in use. Stopping existing Frontend service...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null
fi

echo ""

# Install dependencies if needed
echo -e "${GREEN}Step 1: Installing dependencies...${NC}"

if [ ! -d "Backend/node_modules" ]; then
    echo -e "${BLUE}Installing Backend dependencies...${NC}"
    cd Backend && npm install && cd ..
fi

if [ ! -d "Frontend/node_modules" ]; then
    echo -e "${BLUE}Installing Frontend dependencies...${NC}"
    cd Frontend && npm install && cd ..
fi

echo -e "${GREEN}Dependencies installed!${NC}"
echo ""

# Create .env file for Backend if it doesn't exist
if [ ! -f "Backend/.env" ]; then
    echo -e "${BLUE}Creating Backend .env file...${NC}"
    cp Backend/.env.example Backend/.env
fi

# Start services
echo -e "${GREEN}Step 2: Starting services...${NC}"
echo ""

# Start GenAI Service
echo -e "${BLUE}Starting GenAI Service on port 8000...${NC}"
cd genai-with-agentic-ai
python -m uvicorn main:app --reload --port 8000 > ../logs/genai.log 2>&1 &
GENAI_PID=$!
cd ..
sleep 3

# Start Backend
echo -e "${BLUE}Starting Backend on port 5000...${NC}"
cd Backend
npm run dev > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..
sleep 2

# Start Frontend
echo -e "${BLUE}Starting Frontend on port 5173...${NC}"
cd Frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 3

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           All services are starting up!            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Service URLs:${NC}"
echo -e "  Frontend:  ${GREEN}http://localhost:5173${NC}"
echo -e "  Backend:   ${GREEN}http://localhost:5000${NC}"
echo -e "  GenAI:     ${GREEN}http://localhost:8000${NC}"
echo ""
echo -e "${YELLOW}Process IDs:${NC}"
echo -e "  GenAI PID:    $GENAI_PID"
echo -e "  Backend PID:  $BACKEND_PID"
echo -e "  Frontend PID: $FRONTEND_PID"
echo ""
echo -e "${YELLOW}Logs are being written to ./logs/ directory${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}IMPORTANT: Ingest news articles before using!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "To ingest news, run in a new terminal:"
echo -e "${GREEN}curl 'http://localhost:8000/agent/ingest?url=<NEWS_URL>'${NC}"
echo ""
echo -e "Or run the batch scraper:"
echo -e "${GREEN}curl 'http://localhost:8000/scraper/cron'${NC}"
echo ""
echo -e "${RED}Press Ctrl+C to stop all services${NC}"
echo ""

# Create stop function
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping all services...${NC}"
    kill $GENAI_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}All services stopped!${NC}"
    exit 0
}

trap cleanup INT TERM

# Wait for user interrupt
wait
