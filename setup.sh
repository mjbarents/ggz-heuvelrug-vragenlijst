#!/bin/bash

set -e

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 niet gevonden"
    echo "Installeer met: apt-get install -y python3 python3-pip python3-venv"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "Initializing database..."
python3 init_db.py

echo ""
echo "Setup complete."
echo ""
echo "Start applicatie:"
echo "  source venv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Default admin login: admin / admin"
