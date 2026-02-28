# Inventory System Pro

Inventory System Pro is a full-stack inventory & sales management platform built with **FastAPI** (backend), **Vue 3 + Vite** (frontend), and a **PostgreSQL** datastore. The project ships with end-to-end automation coverage using **Robot Framework** for both API and UI, containerized environments via **Docker Compose**, and seed scripts to bootstrap demo data quickly.

---

## Table of Contents
1. [Highlights](#highlights)
2. [Tech Stack](#tech-stack)
3. [Architecture Overview](#architecture-overview)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Getting Started](#getting-started)
7. [Environment Configuration](#environment-configuration)
8. [Running the Stack](#running-the-stack)
9. [Automation Testing](#automation-testing)
10. [Useful Commands](#useful-commands)
11. [Troubleshooting](#troubleshooting)
12. [Portfolio Checklist](#portfolio-checklist)
13. [Contributing](#contributing)

---

## Highlights

- **Production-like workflows**: Containerized FastAPI, PostgreSQL, and Vite/Nginx mirror a realistic deployment topology.
- **Automated confidence**: Robot Framework covers REST flows plus Selenium UI journeys, enabling repeatable demos.
- **Service layering**: CRUD, services, and schemas clearly separate persistence, business logic, and IO.
- **Batteries included**: Seed scripts, tagged test suites, and `.env` templates shrink onboarding time to minutes.
- **Portfolio ready**: Clean documentation, deterministic commands, and automated testing make this project easy to showcase.

## Tech Stack

| Layer | Technologies |
| --- | --- |
| **API** | FastAPI, SQLAlchemy, Pydantic, Alembic |
| **Data** | PostgreSQL 15 (Alpine), SQL migrations |
| **Frontend** | Vue 3, Vite, Pinia, Vue Router, Bootstrap styles |
| **Automation** | Robot Framework, RequestsLibrary, SeleniumLibrary, ChromeDriver |
| **DevOps** | Docker Compose, Uvicorn, Nginx, seed scripts |

## Architecture Overview

- **Backend**: FastAPI application exposing REST APIs for authentication, product management, transactions, and sales. SQLAlchemy models, Alembic migrations, and service layer encapsulate business logic.
- **Database**: PostgreSQL 15 (Alpine) container, with Alembic handling schema evolution.
- **Frontend**: Vue 3 SPA (Vite tooling) delivering dashboards for inventory & sales, including rich UX features (filters, modals, history tables).
- **Automation**: Robot Framework suites for backend API regression/smoke coverage and Selenium-driven UI flows.
- **Containers**: Docker Compose orchestrates DB, backend (Uvicorn), and frontend (Nginx serving Vite build).

---

## Project Structure

```
inventory-system-pro/
├── backend/                  # FastAPI application
│   ├── app/                  # Core modules, routers, services, schemas
│   ├── scripts/              # Entrypoint & seed utilities
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Vue 3 + Vite SPA
│   ├── src/                  # Views, components, stores
│   ├── package.json
│   └── Dockerfile
├── tests/
│   └── robot/
│       ├── resources/        # Shared keywords & locators
│       └── suites/           # Backend & frontend Robot suites
├── docker-compose.yml        # Orchestrates db/backend/frontend
├── readme.md
└── env/                     # Local Python virtual environment (optional)
```

---

## Prerequisites

- **Docker** & **Docker Compose** (v2+ recommended)
- **Python 3.9+** (only if running backend or Robot tests outside containers)
- **Node 18+** (only if running frontend locally via Vite dev server)

---

## Getting Started

1. **Clone the repository**
	```bash
	git clone https://github.com/<your-org>/inventory-system-pro.git
	cd inventory-system-pro
	```

2. **Copy environment templates**
	```bash
	cp backend/.env.example backend/.env
	cp tests/robot/resources/backend/variables.py.example tests/robot/resources/backend/variables.py
	```

3. **Set secrets & credentials**
	- Update `backend/.env` with `POSTGRES_PASSWORD`, `DATABASE_URL`, and auth seeds.
	- Update `tests/robot/resources/backend/variables.py` with `BASE_URL`, `USERNAME`, `PASSWORD`.

---

## Environment Configuration

`backend/.env` (excerpt):

```
DATABASE_URL=postgresql://postgres:<password>@db/inventory_db
POSTGRES_PASSWORD=<password>
SECRET_KEY=<hex>
USERNAME_SEED=fanfanmyid
PASSWORD_SEED=Sample123!
```

Root `.env` (used by Docker Compose):

```
POSTGRES_PASSWORD=<password>
```

Ensure the values match between backend and Docker configs to avoid auth errors.

---

## Running the Stack

### Option 1: Docker (recommended)

```bash
docker-compose up --build
```

Services exposed:
- Frontend: http://localhost:5173
- Backend API & docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432 (service name `db` inside network)

### Option 2: Local Development

1. **Backend**
	```bash
	cd backend
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	```
2. **Frontend**
	```bash
	cd frontend
	npm install
	npm run dev -- --host
	```
3. Ensure PostgreSQL is running locally or via Docker and matches `DATABASE_URL`.

---

## Automation Testing

### Backend API Suites (Robot Framework)

Run from repository root using the virtual environment or system Python:

```bash
./env/bin/robot -i smoke tests/robot/suites/backend
./env/bin/robot -i regression tests/robot/suites/backend
./env/bin/robot -i feature tests/robot/suites/backend
```

Suite highlights:
- **smoke**: Auth sanity, product availability, IN/OUT transactions.
- **regression**: Transaction BDD, sales checkout flow, product CRUD scenarios.
- **feature**: Comprehensive coverage by pairing smoke + regression tags.

### Frontend UI Suites (Robot + Selenium)

Prerequisites: Chrome/Chromedriver accessible on PATH.

```bash
./env/bin/robot tests/robot/suites/frontend
```

Included suites:
- `login_test.robot`: valid/invalid login flows.
- `dashboard_test.robot`: inventory table, transaction filters, stock modal, logout.
- `sales_test.robot`: sales history visibility & “New Sale” modal.

All suites default to `http://localhost:5173`, so ensure Docker stack or Vite dev server is running.

Robot produces XML/HTML reports under `tests/results/robot`. Attach the HTML log when sharing demo evidence.

---

## Useful Commands

| Task | Command |
| --- | --- |
| Start services | `docker-compose up --build` |
| Stop services | `docker-compose down` |
| Seed database (inside backend container) | `python scripts/seed_db.py` |
| Run Alembic migrations | `alembic upgrade head` |
| Run backend tests (tagged) | `./env/bin/robot -i <tag> tests/robot/suites/backend` |
| Run UI tests | `./env/bin/robot tests/robot/suites/frontend` |

---

## Troubleshooting

- **Auth errors on startup**: Confirm `POSTGRES_PASSWORD` matches across `backend/.env` and root `.env`, then rebuild with `docker-compose up --build`.
- **Database refuses connections**: Run `docker-compose ps` to ensure the `db` health check passes. Use `docker-compose logs db` for detail.
- **Frontend port already in use**: Adjust Vite dev server via `npm run dev -- --host --port 5174` or stop the conflicting process.
- **Robot Selenium failures**: Verify Chrome/Chromedriver versions align and export `CHROMEDRIVER_PATH` if using a custom binary.
- **Stale migrations**: Apply `alembic upgrade head` inside the backend container before seeding data.

---

## Portfolio Checklist

- Capture short clips or animated GIFs of the Dashboard and Sales flows while tests pass in the terminal.
- Mention dual-layer automation (API + UI) and link to the Robot reports in your portfolio site or resume.
- Highlight the Docker-first workflow and the fact that onboarding requires only `docker-compose up --build`.
- Reference this README’s structure in your write-up to show attention to documentation quality.
- Optionally deploy the stack on Fly.io, Render, or Railway and include the public URL for live demos.

---

## Contributing

1. Fork the repo & create a feature branch.
2. Implement changes with tests where applicable.
3. Run lint/tests locally (backend & frontend as needed).
4. Submit a pull request describing the feature/fix, test evidence, and any migration steps.

For bug reports or feature requests, please open an issue with detailed reproduction steps.

---

Maintained with ❤️ to showcase full-stack engineering, DevOps, and automation testing capabilities.