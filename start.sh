#!/bin/bash

echo "🚇 Starting Istanbul Metro Web Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""

# Start the server
echo "🚀 Starting FastAPI server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

cd backend && python3 main.py
