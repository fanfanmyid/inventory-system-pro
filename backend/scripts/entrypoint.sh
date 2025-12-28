#!/bin/sh
set -e

# 1. Wait for Postgres to be ready
echo "--- Checking Database Connection ---"
until python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

if [ ! "$(ls -A /app/alembic/versions/*.py 2>/dev/null)" ]; then
    echo "--- No migrations found. Generating Initial Schema ---"
    python -m alembic revision --autogenerate -m "initial_schema"
fi

# 2. Run Migrations
echo "--- Running Migrations ---"
python -m alembic upgrade head

# 3. Verify Migrations (Optional but good for QA)
echo "--- Migrations Complete. Seeding Database ---"

# 4. Run Seed using Module Mode
export PYTHONPATH=$PYTHONPATH:/app
python -m scripts.seed_db

# 5. Start Server
echo "--- Starting Application ---"
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000