#!/bin/bash
# =============================================================================
# Build Script - TEMPLATE
# =============================================================================
# IT Agent: Customize this script for your project's technology stack.
#
# Instructions:
# 1. Identify the project's build system (from Architect's tech stack decision)
# 2. Add the appropriate build commands below
# 3. Remove these instructions when done
#
# Examples by technology:
# - Node.js:    npm run build
# - Python:     pip install -e . OR python setup.py build
# - Go:         go build ./...
# - Rust:       cargo build --release
# - Java:       mvn package OR gradle build
# - C/C++:      make release
# - Web/Static: No build needed, or use bundler (webpack, vite, etc.)
#
# =============================================================================

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$ROOT_DIR/modules/startup-roaster"

echo "=========================================="
echo "Building Startup Idea Roaster..."
echo "=========================================="

npm install --prefix "$APP_DIR/frontend"
npm run build --prefix "$APP_DIR/frontend"

echo "Build complete. Output: $APP_DIR/frontend/dist"
