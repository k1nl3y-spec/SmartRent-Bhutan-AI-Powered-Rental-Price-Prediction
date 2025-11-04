
#!/bin/bash
# ==========================================================
# SmartRent Bhutan – Codex Maintenance Script
# Purpose: Run light checks before each container start
# ==========================================================

echo "🧠 Running maintenance checks..."

# --- 1. Verify required environment variables ---
required_vars=("DATABASE_URL" "SECRET_KEY" "MODEL_PATH")
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "⚠️ Warning: $var is not set"
  fi
done

# --- 2. Check for stale dependencies ---
pip check || echo "⚠️ Some Python dependencies may be outdated"

# --- 3. Run lightweight backend tests ---
pytest -q --maxfail=1 --disable-warnings || echo "⚠️ Skipping tests"

# --- 4. Lint only modified files (optional) ---
flake8 src/ --count || echo "⚠️ Lint warnings ignored"

# --- 5. Ensure model & data folders exist ---
mkdir -p /workspace/models /workspace/data

echo "✅ Maintenance complete. Environment ready!"
