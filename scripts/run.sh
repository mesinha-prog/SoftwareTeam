#!/bin/bash
# =============================================================================
# Run Script — Startup Idea Roaster
# =============================================================================

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$ROOT_DIR/modules/startup-roaster"

# Load environment variables
if [ -f "$APP_DIR/.env" ]; then
  set -a; source "$APP_DIR/.env"; set +a
fi

# Find available backend port starting from 3001
PORT=3001
while lsof -i :$PORT 2>&1 | grep -q LISTEN; do
  PORT=$((PORT + 1))
done
export PORT

echo "=========================================="
echo "Starting Startup Idea Roaster..."
echo "Backend port: $PORT"
echo "=========================================="

# Update vite proxy target to match detected backend port
sed -i.bak "s|target: 'http://localhost:[0-9]*'|target: 'http://localhost:$PORT'|" "$APP_DIR/frontend/vite.config.js"
rm -f "$APP_DIR/frontend/vite.config.js.bak"

# Open browser after delay
(sleep 5 && open "http://localhost:5173") &

# Start backend and frontend together
cd "$APP_DIR" && npm run dev
