# Tasks

## 1. Map API scaffold

- [x] 1.1 Add Pydantic schemas for map station list response (`stations`, `availability_by_type` fields per design); verify `from app.schemas.map import ...` imports in a smoke import or existing test module.
- [x] 1.2 Register `app/api/map.py` on `api_router` with `GET /stations` stub returning empty list; verify OpenAPI shows `/api/v1/map/stations` at `http://localhost:8000/docs`.

## 2. Load map stations (RF-MP-2, RF-MP-4)

- [x] 2.1 Write API test **Scenario: Empty network returns no stations**; verify it fails before `MapService` aggregates data.
- [x] 2.2 Implement `MapService` station list assembly and wire `GET /map/stations`; verify empty-network test passes.
- [x] 2.3 Write API test **Scenario: Seeded network returns five landmarks** (use `POST /api/v1/seed`); verify it fails until coordinates and names match landmark catalog.
- [x] 2.4 Extend `MapService` to return all seeded stations with lat/lon from DB; verify seeded scenario passes.

## 3. Available count follows fleet (RF-MP-3)

- [x] 3.1 Write API test **Scenario: Parked vehicles increase available count**; verify it fails before count logic exists.
- [x] 3.2 Implement parked-vehicle counts grouped by `(station, vehicle_type)`; verify scenario passes.
- [x] 3.3 Write API test **Scenario: Vehicle out on open rental is excluded**; verify it fails until open-rental vehicles are omitted.
- [x] 3.4 Ensure vehicles with `parked_station_id` null are excluded from counts; verify scenario passes.

## 4. Catalog types and capacity display on API (RF-MP-3)

- [x] 4.1 Write API test **Scenario: Missing type appears with zero**; verify it fails before zero-fill for all catalog types.
- [x] 4.2 Fill missing `(station, type)` pairs with `available_count` `0`, stable order by type name; verify scenario passes.
- [x] 4.3 Write API test **Scenario: Count exceeds stored capacity**; verify it fails if counts are capped by capacity.
- [x] 4.4 Confirm response includes stored `capacity` unchanged and uncapped counts; verify scenario passes.

## 5. Frontend scaffold (RF-MP-1)

- [x] 5.1 Create `frontend/` with Vite + React + TypeScript, `react-leaflet`, and Leaflet CSS; verify `npm run build` succeeds locally.
- [x] 5.2 Add `VITE_API_BASE_URL` defaulting to `http://localhost:8000` and a typed client for `GET /api/v1/map/stations`; verify dev server starts on port `5173`.

## 6. Map client behavior (RF-MP-1–3)

- [x] 6.1 Implement single fetch on mount (no refetch on marker click); verify in browser DevTools Network tab only one map request on load after manual open.
- [x] 6.2 Render OSM tile layer without API key and one marker per station at API coordinates; verify marker for `"Plaza Independencia"` at `-37.32140`, `-59.13310` after seed.
- [x] 6.3 Call Leaflet `fitBounds` when `stations.length > 0`; verify all five seeded markers visible without manual zoom after seed.
- [x] 6.4 Show basemap plus “no stations” message when `stations` is empty; verify message with empty DB and no seed.
- [x] 6.5 Selection panel shows name, capacity, and each type with `available_count` from loaded data; verify `"Centro"`-style content against a station with mixed counts including zero.

## 7. Docker and documentation

- [x] 7.1 Add `frontend` service to `docker-compose.yml` (Vite dev on `5173`, `--host 0.0.0.0`); verify `docker compose up` serves UI and map can reach API on host port `8000`.
- [x] 7.2 Update README with map URL, seed-then-open flow, and manual UI test plan for map-client scenarios; verify documented commands match compose ports.
- [x] 7.3 Run `docker compose build api` and `docker compose --profile test run --rm test`; verify full pytest suite passes.

## Workflow follow-up

- Archive with `openspec archive` after review when Docker pytest is green and manual map checks are done.
