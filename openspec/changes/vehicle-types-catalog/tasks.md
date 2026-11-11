# Tasks

## 1. Backend scaffolding

- [ ] 1.1 Add Python project layout (`backend/`), dependencies (FastAPI, SQLModel, psycopg, uvicorn, httpx, pytest), and `docker-compose.yml` for API + PostgreSQL; verify `docker compose build` succeeds.
- [ ] 1.2 Add FastAPI app factory, DB engine/session from env, and `VehicleType` SQLModel table (`create_all` on startup for dev/test); verify app starts and `GET /health` returns 200 inside Compose.
- [ ] 1.3 Add pytest config and HTTP client fixture (per-test DB or transaction rollback); verify an empty `pytest` run collects tests and exits 0.

## 2. Add and list (RF-VT-1)

- [ ] 2.1 Write API test **Scenario: Add type with name and rate** (`"Bici urbana"`, `150`); verify test fails before implementation.
- [ ] 2.2 Implement `POST /api/v1/vehicle-types` and response model; verify scenario test passes.
- [ ] 2.3 Write API test **Scenario: List after one add** (`"Monopatín"`, `220`); verify test fails if list not implemented.
- [ ] 2.4 Implement `GET /api/v1/vehicle-types` and `GET /api/v1/vehicle-types/{id}`; verify list scenario test passes.

## 3. Rename (RF-VT-2)

- [ ] 3.1 Write API test **Scenario: Rename preserves rate**; verify test fails before PATCH name exists.
- [ ] 3.2 Implement PATCH for `name` on `/api/v1/vehicle-types/{id}`; verify rename scenario test passes.

## 4. Current rate update (RF-VT-3)

- [ ] 4.1 Write API test **Scenario: Rate update changes stored current rate** (`150` → `180`); verify test fails before PATCH rate exists.
- [ ] 4.2 Implement PATCH for `current_rate`; verify rate scenario test passes.

## 5. Fleet usage port and delete unused (RF-VT-4)

- [ ] 5.1 Define `FleetUsagePort` and `StubFleetUsage` (always unused); wire into app dependencies; verify unit test on stub returns `False`.
- [ ] 5.2 Write API test **Scenario: Delete when fleet reports no usage**; verify test fails before DELETE exists.
- [ ] 5.3 Implement `DELETE /api/v1/vehicle-types/{id}` with stub port; verify delete-success scenario test passes.

## 6. Delete refused (RF-VT-5)

- [ ] 6.1 Write API test **Scenario: Delete refused when fleet reports usage** using injectable fake port (`409`, type still listed); verify test fails before conflict handling exists.
- [ ] 6.2 Implement delete guard and `409` response when port reports in use; verify refuse scenario test passes.

## 7. Validation and suite

- [ ] 7.1 Add request validation tests (empty name, negative rate → `422`); verify they pass.
- [ ] 7.2 Run full `pytest` in Docker against PostgreSQL; verify entire suite passes.

## Workflow follow-up

- Archive the change with `openspec archive` after review, when the full pytest suite passes locally in Docker.
