# GreenWheels

Local vehicle-rental system for one city (learning project). See [requirements.md](requirements.md) for product scope.

**Stack:** Python (FastAPI, SQLModel), PostgreSQL, Alembic, React (Vite + Leaflet), Docker. OpenSpec specs live under `openspec/`.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose (Docker Desktop on Windows/macOS includes Compose).

## Docker (recommended)

From the repository root:

```bash
# Build images (api is shared by api and test services)
docker compose build api
docker compose build frontend

# Start database, API, and map UI
docker compose up -d

# Run tests against PostgreSQL
docker compose --profile test run --rm test

# Stop services
docker compose down
```

| Service | URL / port |
|---------|----------------|
| Station map (UI) | http://localhost:5173 |
| API | http://localhost:8000 |
| OpenAPI docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |
| PostgreSQL (from the host) | `localhost:5433` (user `greenwheels`, password `greenwheels`, db `greenwheels`) |

Containers talk to Postgres on `db:5432` inside the Compose network; only the host mapping uses **5433** to avoid clashing with a local PostgreSQL on 5432.

The `api` container runs **`alembic upgrade head`** before starting Uvicorn. The `test` profile does the same before pytest.

### Database migrations

From `backend/` (or inside the `api` container at `/app`):

```bash
# Apply all revisions
alembic upgrade head

# New revision after model changes (review autogenerate output)
alembic revision --autogenerate -m "describe change"
```

If you previously used `create_all` only and migrations fail on an old volume, reset dev data:

```bash
docker compose down -v
docker compose up -d --build
```

## API (current slice)

Vehicle types catalog:

- `POST/GET/PATCH/DELETE` → `/api/v1/vehicle-types`

Stations network:

- `POST/GET/PATCH/DELETE` → `/api/v1/stations`

Fleet (parked vehicles):

- `POST/GET/PATCH/DELETE` → `/api/v1/vehicles`

Rentals:

- `POST` → `/api/v1/rentals/checkout`
- `POST` → `/api/v1/rentals/{id}/return`
- `POST` → `/api/v1/rentals/{id}/record-payment`
- `GET` → `/api/v1/rentals`, `/api/v1/rentals/{id}`

Demo network seed (empty database only):

- `POST` → `/api/v1/seed` — creates five Tandil landmark stations, four demo vehicle types, fifty vehicles, and five open rentals. Returns **409** if any station, vehicle type, vehicle, or rental already exists (no reset endpoint).

Station map:

- `GET` → `/api/v1/map/stations` — stations with coordinates, capacity, and available counts for every vehicle type (zero when none are parked).

### Map workflow

1. Start stack: `docker compose up -d` (or API + DB only if using the frontend locally).
2. On an **empty** database, seed once: `POST http://localhost:8000/api/v1/seed` (or use Swagger at `/docs`).
3. Open **http://localhost:5173** — OpenStreetMap with station markers; click a marker for name, capacity, and per-type availability.

The UI loads `/api/v1/map/stations` **once** on open. Override the API URL with `VITE_API_BASE_URL` (see `frontend/.env.example`). The browser must reach the API on the host (`http://localhost:8000`); Compose sets this for the `frontend` service.

**Manual UI checks (v1):**

- Empty DB: basemap + “No stations exist”, no markers.
- After seed: five markers, view fits all stations, panel shows capacity and all four types (some counts may be zero).
- Network tab: exactly one map stations request on reload.

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
cd backend
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend (optional, without Docker)

```bash
cd frontend
cp .env.example .env
npm ci
npm run dev
```

Map dev server: http://localhost:5173 (API must be running with CORS for port 5173).

## OpenSpec workflows

Planning and implementation are driven by OpenSpec changes under `openspec/changes/`. Typical commands in the IDE: `/opsx-propose`, `/opsx-apply`, `/opsx-archive`.
