#!/bin/bash
# =============================================================================
# Test Script - TEMPLATE
# =============================================================================
# IT Agent: Customize this script for your project's test framework.
#
# Instructions:
# 1. Identify the project's test framework (from Architect's tech stack decision)
# 2. Add the appropriate test commands below
# 3. Remove these instructions when done
#
# Examples by technology:
# - Node.js:    npm test OR jest OR mocha
# - Python:     pytest OR python -m unittest
# - Go:         go test ./...
# - Rust:       cargo test
# - Java:       mvn test OR gradle test
# - C/C++:      make test OR ctest
#
# =============================================================================

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$ROOT_DIR/modules/startup-roaster"

echo "=========================================="
echo "Running Startup Idea Roaster tests..."
echo "=========================================="

npm test --prefix "$APP_DIR/frontend"
