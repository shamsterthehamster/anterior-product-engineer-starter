#!/bin/bash
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -f .env.local ]; then
    source .env.local
    echo "✅ Environment variables loaded."
fi

# Install prerequisites
echo "Setting up development environment..."

# Check for required system dependencies
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi


# Backend setup
echo "Installing backend dependencies..."
cd backend
python3 -m pip install -r requirements.txt
cd ..

# Frontend setup
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Ensure PostgreSQL database exists
echo "📂 Checking database..."
python3 database_creation_script.py

# Apply Alembic migrations
echo "🔄 Running database migrations..."
alembic upgrade head

echo "✅ Setup complete! Your development environment is ready."

# Run frontend and backend servers
echo "Starting frontend server..."
osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR/frontend' && npm run dev\""# cd frontend

echo "Starting backend server..."
osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR/backend' && source '$PROJECT_DIR/.env.local' && python3 -muvicorn main:app --reload\""

echo "✅ All servers are running! Your development environment is ready."
