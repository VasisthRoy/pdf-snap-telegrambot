#!/bin/bash
# Quick Start Script for PDF Telegram Bot
# This script automates the initial setup process

echo "🚀 PDF Telegram Bot - Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.9 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detected"

# Check if poppler is installed
if ! command -v pdftoppm &> /dev/null; then
    echo "⚠️  poppler-utils not found!"
    echo ""
    echo "Installing system dependencies..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y poppler-utils
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install poppler
    else
        echo "❌ Unsupported OS. Please install poppler-utils manually."
        echo "   Windows: https://github.com/oschwartz10612/poppler-windows/releases/"
        exit 1
    fi
fi

echo "✅ poppler-utils installed"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment created"
echo ""

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your bot token!"
    echo "   Get your token from @BotFather on Telegram"
    echo ""
    
    # Try to open .env in default editor
    if command -v nano &> /dev/null; then
        read -p "Would you like to edit .env now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            nano .env
        fi
    fi
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Make sure you added your BOT_TOKEN to .env file"
echo "2. Run the bot with: python bot.py"
echo "3. Open Telegram and start chatting with your bot!"
echo ""
echo "Need help? Check README.md for detailed instructions."
echo ""
