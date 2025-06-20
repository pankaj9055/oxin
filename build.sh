#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r pyproject.toml

# Create necessary directories
mkdir -p static/uploads
mkdir -p instance

echo "Build completed successfully!"