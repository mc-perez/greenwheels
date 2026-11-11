# GreenWheels

Local vehicle-rental system for one city (learning project). See [requirements.md](requirements.md) for product scope.

**Stack:** Python (FastAPI, SQLModel), PostgreSQL, Docker. OpenSpec specs live under `openspec/`.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose (Docker Desktop on Windows/macOS includes Compose).

## Docker (recommended)

From the repository root:

```bash
# Build images
docker compose build

# Start database and API
docker compose up -d

# Run tests against PostgreSQL
docker compose --profile test run --rm test

# Stop services
docker compose down
```

| Service | URL / port |
|---------|----------------|
| API | http://localhost:8000 |
| OpenAPI docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |
| PostgreSQL (from the host) | `localhost:5433` (user `greenwheels`, password `greenwheels`, db `greenwheels`) |

Containers talk to Postgres on `db:5432` inside the Compose network; only the host mapping uses **5433** to avoid clashing with a local PostgreSQL on 5432.

## API (current slice)

Vehicle types catalog:

- `POST/GET/PATCH/DELETE` → `/api/v1/vehicle-types`

## Local tests without Docker (optional)

Uses in-memory SQLite when `DATABASE_URL` is unset.

```bash
cd backend
python -m venv .venv
```

**macOS / Linux:**

```bash
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
```

To run the API locally against Postgres in Docker, set `DATABASE_URL` (for example in `backend/.env`):

```text
DATABASE_URL=postgresql+psycopg://greenwheels:greenwheels@localhost:5433/greenwheels
```

```bash
uvicorn app.main:app --reload --app-dir backend
```

## OpenSpec workflows

Planning and implementation are driven by OpenSpec changes under `openspec/changes/`. Typical commands in the IDE: `/opsx-propose`, `/opsx-apply`, `/opsx-archive`.
