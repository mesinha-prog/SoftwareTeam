#!/bin/bash
# =============================================================================
# Clean Script - TEMPLATE
# =============================================================================
# IT Agent: Customize this script to clean build artifacts.
#
# Instructions:
# 1. Identify what build artifacts the project creates
# 2. Add the appropriate clean commands below
# 3. Remove these instructions when done
#
# Examples by technology:
# - Node.js:    rm -rf node_modules dist .next
# - Python:     rm -rf __pycache__ *.egg-info .pytest_cache dist build
# - Go:         go clean OR rm -rf bin/
# - Rust:       cargo clean
# - Java:       mvn clean OR gradle clean
# - C/C++:      make clean
#
# Common directories to clean:
# - output/release/*
# - output/debug/*
# - modules/*/release/*
# - modules/*/debug/*
#
# =============================================================================

echo "=========================================="
echo "Cleaning Startup Idea Roaster artifacts..."
echo "=========================================="

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$ROOT_DIR/modules/startup-roaster"

rm -rf "$APP_DIR/frontend/dist"
rm -rf "$APP_DIR/frontend/node_modules"
rm -rf "$APP_DIR/server/node_modules"
rm -rf "$APP_DIR/node_modules"

echo "Clean complete."
