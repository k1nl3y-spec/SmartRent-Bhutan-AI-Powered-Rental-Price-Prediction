#!/bin/bash
# ==========================================================
# SmartRent Bhutan – Codex Setup Script
# Environment: openai/codex-universal (Ubuntu 24.04)
# Purpose: Install backend + frontend dependencies, lint, and test
# ==========================================================

set -e  # stop on first error

echo "🔧 Setting up SmartRent Bhutan environment..."

# --- 1. Update system packages ---
sudo apt-get update -y && sudo apt-get install -y build-essential python3-dev

# --- 2. Backend (Python / FastAPI) setup ---
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
# If the file is missing, continue instead of crashing
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ No requirements.txt found, installing base packages..."
    pip install fastapi uvicorn pandas scikit-learn sqlalchemy joblib psycopg2-binary python-dotenv pytest flake8
fi

# --- 3. Frontend (Next.js) setup ---
if [ -d "frontend" ]; then
    echo "🌐 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "⚠️ No frontend directory found — skipping Next.js setup."
fi

# --- 4. Create necessary directories ---
mkdir -p /workspace/models /workspace/data /workspace/logs

# --- 5. Optional: preload or download model ---
# python scripts/download_model.py || echo "⚠️ Skipping model preload."

# --- 6. Lint and basic tests ---
echo "🧹 Running lint and tests..."
flake8 src/ || echo "⚠️ Lint warnings ignored."
pytest -q --maxfail=1 --disable-warnings || echo "⚠️ Tests skipped or failed."

echo "✅ Setup complete! Environment ready for caching."
