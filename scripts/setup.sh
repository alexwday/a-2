#!/bin/bash

echo "=========================================="
echo "Multi-Agent Finance Assistant Setup"
echo "=========================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created from .env.example"
    echo ""
    echo "⚠️  Please edit .env and add your configuration:"
    echo "   - For local: Add your OpenAI API key"
    echo "   - For work: Add OAuth credentials and SSL settings"
fi

# Test the setup
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To test the connection:"
echo "  python main.py"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"