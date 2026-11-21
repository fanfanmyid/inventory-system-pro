"""CI smoke check: verify the FastAPI app imports and serves without a database.

Run from the backend/ directory with dummy settings, e.g.:

    DATABASE_URL=postgresql://postgres:***@localhost:5432/inventory_db \
    SECRET_KEY=ci-smoke-secret python scripts/smoke_check.py

Requires httpx (used by fastapi.testclient.TestClient).
This intentionally does NOT touch the database: engine creation is lazy,
so importing the app and hitting non-DB routes proves the wiring works.
"""
import sys
from pathlib import Path

# Allow running as `python scripts/smoke_check.py` from backend/ without
# installing the package or setting PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app


def main() -> int:
    client = TestClient(app)

    root = client.get("/")
    assert root.status_code == 200, f"GET / -> {root.status_code}"
    assert root.json() == {"message": "Inventory API is running"}, root.json()

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200, f"GET /openapi.json -> {openapi.status_code}"
    paths = openapi.json()["paths"]
    expected = {
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/products/",
        "/api/v1/transactions/",
        "/api/v1/sales/",
    }
    missing = expected - set(paths)
    assert not missing, f"Missing API routes: {missing}"

    print(f"Smoke check OK: {len(app.routes)} routes registered, "
          f"{len(paths)} OpenAPI paths, GET / -> 200")
    return 0


if __name__ == "__main__":
    sys.exit(main())
