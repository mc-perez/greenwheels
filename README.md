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

### Operator console

Same app at **http://localhost:5173** — green top nav: **Map**, **Vehicle types**, **Stations**, **Fleet**, **Rentals**. All console actions call the existing REST API (`VITE_API_BASE_URL`, default `http://localhost:8000`).

1. Start stack and seed once (see [Map workflow](#map-workflow)).
2. Use nav links; no full-page navigation away from the app origin.

**Manual UI checks (operator console):**

| Scenario | Steps |
|----------|--------|
| Default map route | Open `/` — map loads; nav shows **Map** active. |
| Add vehicle type | **Vehicle types** → name `Bici urbana`, rate `150` → **Add** → row appears. |
| Delete type in use | After seed, delete a type used by a vehicle → red banner with API message; type remains. |
| Add station | **Stations** → `Centro`, capacity `20`, lat `-37.32167`, lon `-59.13316` → **Add**. |
| Station validation error | Submit coordinates outside Tandil urban area → banner shows API validation/detail; list unchanged. |
| Add parked vehicle | **Fleet** → pick type and station → **Add vehicle**; row shows **Available** Yes. |
| Checkout picker | **Rentals** → **Check out vehicle** → dropdown lists only parked (`available`) vehicles. |
| Checkout success | Confirm checkout for a parked vehicle → new **Open** rental in table. |
| Checkout conflict | Try checkout for a vehicle already **out** (not in picker if only parked are listed; or retry via API) → banner on conflict. |
| Return rental | On an open rental → **Return** → choose station (full stations allowed) → **Closed** with amount. |
| Record payment | On closed, unpaid rental → **Record payment** → **Paid** Yes. |

The map tab does not auto-refresh after rentals; reload **Map** to see updated availability counts.

### MCP (Cursor & OpenCode)

Local **stdio** MCP server in [`mcp-server/`](mcp-server/). It proxies the operator REST API (`GREENWHEELS_API_URL`, default `http://localhost:8000`). Start the API first: `docker compose up -d api db`.

**Setup:**

```powershell
cd mcp-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

POSIX: use `.venv/bin/python` and `scripts/run-mcp.sh`.

**MCP tools**

| Phase | Tool | API |
|-------|------|-----|
| 1 | `health_check` | `GET /health` |
| 1 | `get_map_stations` | `GET /api/v1/map/stations` |
| 1 | `list_vehicle_types` | `GET /api/v1/vehicle-types` |
| 1 | `list_stations` | `GET /api/v1/stations` |
| 1 | `list_vehicles` | `GET /api/v1/vehicles` |
| 1 | `list_rentals` | `GET /api/v1/rentals` |
| 1 | `get_rental` | `GET /api/v1/rentals/{id}` |
| 1 | `checkout_rental` | `POST /api/v1/rentals/checkout` |
| 1 | `return_rental` | `POST /api/v1/rentals/{id}/return` |
| 1 | `record_rental_payment` | `POST /api/v1/rentals/{id}/record-payment` |
| 2 | `create_vehicle_type`, `update_vehicle_type`, `delete_vehicle_type` | `/api/v1/vehicle-types` |
| 2 | `create_station`, `update_station`, `delete_station` | `/api/v1/stations` |
| 2 | `create_vehicle`, `update_vehicle`, `delete_vehicle` | `/api/v1/vehicles` |
| 2 | `seed_network` | `POST /api/v1/seed` (409 if network already exists) |

Tool failures surface API `detail` text (no stack traces).

**Cursor** (`mcpServers`):

```json
{
  "mcpServers": {
    "greenwheels": {
      "command": "c:\\code\\greenwheels\\mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["-m", "greenwheels_mcp"],
      "env": {
        "GREENWHEELS_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

**OpenCode:** copy [`mcp-server/.opencode.jsonc.example`](mcp-server/.opencode.jsonc.example) into project `opencode.jsonc` (adjust `command` to `.venv/bin/python` on Linux/macOS). Or:

```bash
opencode mcp add greenwheels --env GREENWHEELS_API_URL=http://localhost:8000 -- mcp-server/.venv/Scripts/python.exe -m greenwheels_mcp
```

Use `codemode: false` in config for direct tool calls. Verify: `opencode mcp list` with API running; invoke `list_stations` after seed.

**MCP tests:** `cd mcp-server` → `pytest -q` (HTTP mocked with respx).

## Tests

| Layer | What runs | Command |
|-------|-----------|---------|
| **API** (official) | `pytest` on PostgreSQL (migrations + app) | `docker compose --profile test run --rm test` |
| **API** (local fast) | `pytest` on in-memory SQLite | `cd backend` → venv → `pytest -q` |
| **API** (local + Postgres) | `pytest` against Compose `db` on host port 5433 | Set `DATABASE_URL`, then `pytest -q` |
| **Frontend** | Typecheck + production build, lint | `cd frontend` → `npm run build`, `npm run lint` |
| **Map UI** | Manual checks only (no e2e in CI) | See [Map workflow](#map-workflow) above |
| **Operator console UI** | Manual checks only | See [Operator console](#operator-console) above |
| **MCP** | `pytest` in `mcp-server/` (respx) | `cd mcp-server` → `pytest -q`; hosts: manual `opencode mcp list` / Cursor MCP |
| **Database** | Alembic + migration tests | Covered by API `pytest` (e.g. `test_database_migrations.py`) |

All automated product behavior is tested in **`backend/tests/`** with pytest. The `test` Compose service uses the same image as `api` and runs `alembic upgrade head` before pytest.

### Backend — Docker + PostgreSQL (recommended)

From the repository root:

```bash
docker compose build api
docker compose --profile test run --rm test
```

Target one file or test (still from repo root):

```bash
docker compose --profile test run --rm test sh -c "python -m alembic upgrade head && pytest -q tests/test_map_stations.py"

docker compose --profile test run --rm test sh -c "python -m alembic upgrade head && pytest -q tests/test_map_stations.py::test_empty_network_returns_no_stations"
```

On Windows PowerShell the same `docker compose` lines apply.

### Backend — local (without Docker for pytest)

Uses in-memory SQLite when `DATABASE_URL` is unset (quick feedback; Postgres suite is the source of truth in CI).

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

Against Postgres from `docker compose up -d db` (host port **5433**):

```text
DATABASE_URL=postgresql+psycopg://greenwheels:greenwheels@localhost:5433/greenwheels
```

```bash
cd backend
alembic upgrade head
pytest -q
```

### Frontend

No Playwright or e2e tests in v1. Verify compile and lint:

```bash
cd frontend
npm ci
npm run build
npm run lint
```

### Database smoke check (optional)

Postgres health only (not an application test):

```bash
docker compose up -d db
docker compose exec db pg_isready -U greenwheels -d greenwheels
```

## Local development (without Docker for the app)

### API

```bash
cd backend
alembic upgrade head
uvicorn app.main:app --reload
```

Use `DATABASE_URL` pointing at Compose Postgres when the DB runs in Docker (see [Tests](#tests)).

### Frontend

```bash
cd frontend
cp .env.example .env   # Windows: copy .env.example .env
npm ci
npm run dev
```

Map dev server: http://localhost:5173 (API must be running with CORS for port 5173).

## OpenSpec workflows

Planning and implementation are driven by OpenSpec changes under `openspec/changes/`. Typical commands in the IDE: `/opsx-propose`, `/opsx-apply`, `/opsx-archive`.
