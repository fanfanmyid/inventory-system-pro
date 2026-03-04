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

STAMP_NEEDED=$(python - <<'PY'
import os
from sqlalchemy import create_engine, inspect, text

database_url = os.environ.get("DATABASE_URL")
engine = create_engine(database_url)

with engine.connect() as connection:
  inspector = inspect(connection)
  tables = set(inspector.get_table_names())

  business_tables = {"users", "products", "transactions", "sales", "sale_items"}
  schema_exists = any(table in tables for table in business_tables)
  has_alembic_table = "alembic_version" in tables

  needs_stamp = False
  if schema_exists:
    if not has_alembic_table:
      needs_stamp = True
    else:
      try:
        current_revision = connection.execute(text("SELECT version_num FROM alembic_version LIMIT 1")).scalar()
        if not current_revision:
          needs_stamp = True
      except Exception:
        needs_stamp = True

  print("yes" if needs_stamp else "no")
PY
)

if [ "$STAMP_NEEDED" = "yes" ]; then
  echo "--- Existing schema detected without a valid Alembic stamp. Stamping to head ---"
  python -m alembic stamp head
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