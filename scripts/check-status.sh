#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     ML-Powered AI News Platform - Status Check    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Check GenAI Service
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "🤖 GenAI API (8000):  ${GREEN}✓ Running${NC}  http://localhost:8000"
else
    echo -e "🤖 GenAI API (8000):  ${RED}✗ Stopped${NC}"
fi

# Check Backend Service
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "⚙️  Backend (5000):    ${GREEN}✓ Running${NC}  http://localhost:5000"
else
    echo -e "⚙️  Backend (5000):    ${RED}✗ Stopped${NC}"
fi

# Check Frontend Service
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "🌐 Frontend (5173):   ${GREEN}✓ Running${NC}  http://localhost:5173"
else
    echo -e "🌐 Frontend (5173):   ${RED}✗ Stopped${NC}"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Count running services
RUNNING=0
lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 && ((RUNNING++))
lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 && ((RUNNING++))
lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1 && ((RUNNING++))

if [ $RUNNING -eq 3 ]; then
    echo -e "${GREEN}✅ All services are running!${NC}"
    echo ""
    echo "Access the application at: http://localhost:5173"
elif [ $RUNNING -eq 0 ]; then
    echo -e "${RED}❌ No services are running${NC}"
    echo ""
    echo "Start all services with: ./scripts/start-all.sh"
else
    echo -e "${YELLOW}⚠️  Only $RUNNING/3 services are running${NC}"
    echo ""
    echo "Restart all services with: ./scripts/start-all.sh"
fi

echo ""
