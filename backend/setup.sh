#!/bin/bash

# AI Chatbox - Quick Setup Script
# This script helps set up the backend quickly

set -e

echo "🚀 AI Chatbox Backend Setup"
echo "================================"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ is required. You have Python $python_version"
    exit 1
fi
echo "✅ Python $python_version detected"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys!"
    echo "    - OPENAI_API_KEY"
    echo "    - ANTHROPIC_API_KEY"
    echo "    - GOOGLE_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Check PostgreSQL
echo ""
echo "Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL is installed"
    
    # Try to connect
    if psql -lqt | cut -d \| -f 1 | grep -qw chatbot; then
        echo "✅ Database 'chatbot' exists"
    else
        echo "⚠️  Database 'chatbot' not found"
        echo "Creating database..."
        createdb chatbot 2>/dev/null || echo "Note: You may need to create the database manually"
    fi
else
    echo "⚠️  PostgreSQL is not installed or not in PATH"
    echo "Please install PostgreSQL 15+ and create a database named 'chatbot'"
fi

# Check Redis
echo ""
echo "Checking Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis is running"
    else
        echo "⚠️  Redis is installed but not running"
        echo "Please start Redis with: redis-server"
    fi
else
    echo "⚠️  Redis is not installed"
    echo "Please install Redis 7+"
fi

# Summary
echo ""
echo "================================"
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Make sure PostgreSQL and Redis are running"
echo "3. Run the server:"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "4. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "Happy coding! 🎉"
