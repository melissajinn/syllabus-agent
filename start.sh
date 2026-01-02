#!/bin/sh

# Install backend deps
pip install --no-cache-dir -r backend/requirements.txt

# Install frontend deps
cd frontend
npm install
cd ..

# Start backend in background
uvicorn backend.main:app --host 0.0.0.0 --port $PORT

# # Start frontend (foreground – keeps container alive)
# cd frontend
# npm run dev -- --host 0.0.0.0 --port $PORT
