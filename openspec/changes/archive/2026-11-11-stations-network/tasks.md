# Tasks

## 1. Schema, geo constants, and ports

- [x] 1.1 Add `app/geo/tandil.py` with urban bbox constants and `is_inside_tandil_urban`; unit-test boundary inclusivity at edges and rejection outside.
- [x] 1.2 Define `StationFleetUsagePort` and `StubStationFleetUsage`; wire stub in dependencies; unit-test stub returns `False`.
- [x] 1.3 Add Alembic revision creating `station` table and `UNIQUE` on `station.name` and `vehicle_type.name`; verify `alembic upgrade head` on empty DB and migration test passes.

## 2. Add and list stations (RF-ST-2)

- [x] 2.1 Write API test **Scenario: Add station with name, capacity, and urban coordinates**; verify it fails before `POST /api/v1/stations` exists.
- [x] 2.2 Implement `Station` model, repository, service, schemas, and `POST /api/v1/stations`; verify add scenario passes.
- [x] 2.3 Write API test **Scenario: List after one add**; verify it fails before list exists.
- [x] 2.4 Implement `GET /api/v1/stations` and register router; verify list scenario passes.

## 3. Get station (RF-ST-3)

- [x] 3.1 Write API test **Scenario: Get existing station** and 404 for unknown id; verify tests fail before get route.
- [x] 3.2 Implement `GET /api/v1/stations/{id}`; verify get scenario passes.

## 4. Update station (RF-ST-4, RF-ST-6)

- [x] 4.1 Write API test **Scenario: Update capacity preserves name and location**; verify fails before PATCH.
- [x] 4.2 Implement PATCH for `name`, `capacity`, `latitude`, `longitude`; verify update scenario passes.
- [x] 4.3 Write API test **Scenario: Update capacity below any future occupancy is allowed**; verify passes after PATCH.

## 5. Urban bounding box (RF-ST-7)

- [x] 5.1 Write API tests **Scenario: Reject latitude south of urban south edge** and **Scenario: Reject longitude west of urban west edge**; verify fail before validation.
- [x] 5.2 Enforce bbox on create and location fields on PATCH via Pydantic/service; verify bbox scenarios pass.

## 6. Unique station names (RF-ST-1)

- [x] 6.1 Write API tests **Scenario: Reject add with duplicate station name** and **Scenario: Reject rename to another station's name**; verify fail before conflict handling.
- [x] 6.2 Return `409` on duplicate name (service + DB); verify duplicate scenarios pass.

## 7. Delete station with fleet port (RF-ST-5)

- [x] 7.1 Write API test **Scenario: Delete when fleet reports no vehicles at station**; verify fails before DELETE.
- [x] 7.2 Implement `DELETE /api/v1/stations/{id}` with stub port; verify delete-success scenario passes.
- [x] 7.3 Write API test **Scenario: Delete refused when fleet reports usage** with injectable fake port; verify fails before `409` handling.
- [x] 7.4 Implement delete guard and `409` when port reports usage; verify refuse scenario passes.

## 8. Unique vehicle type names (RF-VT-6)

- [x] 8.1 Write API tests **Scenario: Reject add with duplicate type name** and **Scenario: Reject rename to another type's name**; verify fail before uniqueness enforcement.
- [x] 8.2 Implement `409` on duplicate vehicle type name on create and rename; verify scenarios pass.

## 9. Validation and suite

- [x] 9.1 Add validation tests for empty name, capacity `< 1`, invalid Earth lat/lon → `422`; verify pass.
- [x] 9.2 Run full `pytest` in Docker against PostgreSQL; verify entire suite passes.

## Workflow follow-up

- Archive the change with `openspec archive` after review, when the full pytest suite passes locally in Docker.
