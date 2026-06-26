#!/bin/bash

set -e

command -v python3 >/dev/null 2>&1 || {
    echo "Python3 is not installed."
    exit 1
}

echo "🚀 FalconValley Setup"
echo "====================="

# ساخت virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# فعال‌سازی venv
source venv/bin/activate

# نصب پکیج‌ها
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# ساخت .env از روی .env.example
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "✏️ Please edit .env and fill in your values."
    echo "Then run:"
    echo "source venv/bin/activate && python run.py"
else
    echo "✅ .env already exists"
    echo ""
    echo "▶️ To start the bot:"
    echo "source venv/bin/activate && python run.py"
fi

echo ""
echo "✅ Setup complete!"
