#!/bin/bash

# Second Brain - Start Backend API Server
# This script starts the Python backend that the Swift app communicates with

echo "=========================================="
echo "🧠 Second Brain Backend Starter"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start Qdrant in Docker if not running
if ! docker ps | grep -q "qdrant"; then
    echo "🐳 Starting Qdrant database..."
    docker-compose up -d
    sleep 2
fi

# Start the Python API backend
echo "🚀 Starting API backend on http://127.0.0.1:5555"
echo "=========================================="
python api_backend.py

