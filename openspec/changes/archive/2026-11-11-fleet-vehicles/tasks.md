# Tasks

## 1. Schema and migrations

- [x] 1.1 Write migration test assertion for `vehicle` table after `0003`; verify it fails before the revision exists.
- [x] 1.2 Add Alembic revision `0003_*` creating `vehicle` with FKs to `vehicle_type` and `station` (`parked_station_id` nullable); verify migration test and `alembic upgrade head` on empty DB pass.

## 2. Add parked vehicle (RF-FL-4, RF-FL-2)

- [x] 2.1 Write API tests **Scenario: Add vehicle with type and parked station**, **Scenario: Reject add with unknown vehicle type**, and **Scenario: Reject add with unknown station**; verify they fail before `POST /api/v1/vehicles` exists.
- [x] 2.2 Implement `Vehicle` model, repository, service, schemas, and `POST /api/v1/vehicles`; register router; verify add and reject scenarios pass.

## 3. List and get (RF-FL-4)

- [x] 3.1 Write API tests **Scenario: List after one add** and **Scenario: Get existing vehicle** (plus 404 for unknown id); verify fail before routes exist.
- [x] 3.2 Implement `GET /api/v1/vehicles` and `GET /api/v1/vehicles/{id}` with `available` on reads; verify scenarios pass.

## 4. Update parked vehicle (RF-FL-4)

- [x] 4.1 Write API tests **Scenario: Update parked station preserves type**, **Scenario: Update vehicle type preserves parked station**, and **Scenario: Reject update with unknown station**; verify fail before PATCH.
- [x] 4.2 Implement PATCH for `vehicle_type_id` and/or `station_id`; verify update scenarios pass.

## 5. Delete vehicle (RF-FL-4)

- [x] 5.1 Write API test **Scenario: Delete existing vehicle**; verify fails before DELETE.
- [x] 5.2 Implement `DELETE /api/v1/vehicles/{id}`; verify delete scenario passes.

## 6. Availability (RF-FL-3)

- [x] 6.1 Write API test **Scenario: Parked vehicle is available** on create/get responses; verify passes after reads include `available`.

## 7. Capacity is not a gate (RF-FL-6)

- [x] 7.1 Write API test **Scenario: Park when stored capacity is already exceeded**; verify fails before create allows second park.
- [x] 7.2 Ensure service does not compare parked count to `station.capacity`; verify scenario passes.

## 8. Fleet usage ports (RF-FL-5)

- [x] 8.1 Write API tests **Scenario: Type delete refused when a vehicle uses the type** and **Scenario: Type delete succeeds when no vehicle uses the type** using real vehicles (no fake port); verify fail before SQL port wiring.
- [x] 8.2 Write API tests **Scenario: Station delete refused when a vehicle is parked there** and **Scenario: Station delete succeeds when no vehicle is parked there** using real vehicles; verify fail before SQL port wiring.
- [x] 8.3 Implement SQL-backed `FleetUsagePort` and `StationFleetUsagePort`; wire as defaults in `dependencies.py`; verify integration scenarios pass and existing fake-port delete tests still pass.

## 9. Suite and docs

- [x] 9.1 Register `Vehicle` model in metadata/conftest; add `conftest` helpers for type + station + vehicle where useful.
- [x] 9.2 Run full `docker compose --profile test run --rm test`; verify entire suite passes.
- [x] 9.3 Update README API slice to include `/vehicles` endpoints; verify paths match OpenAPI.

## Workflow follow-up

- Archive the change with `openspec archive` after review when the full pytest suite passes locally in Docker.
