#!/bin/sh
set -e

# Install backend deps
pip install --no-cache-dir -r requirements.txt

# Start backend - app.py is in src/ folder
uvicorn src.app:app --host 0.0.0.0 --port $PORT