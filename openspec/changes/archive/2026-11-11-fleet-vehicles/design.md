# Design

## Context

See `proposal.md` for motivation. The backend exposes `/api/v1/vehicle-types` and `/api/v1/stations` with Alembic through `0002_stations_and_unique_names`. Delete paths call `FleetUsagePort` and `StationFleetUsagePort`, currently stubbed to always report no usage. This change adds the `vehicle` table, fleet API, and SQL-backed port implementations.

## Goals / Non-Goals

**Goals:**

- Persist vehicles (`id`, `vehicle_type_id`, `parked_station_id` nullable for future Rental).
- CRUD-style API for parked vehicles mirroring existing catalog patterns.
- Wire real fleet usage queries into default dependencies; keep test overrides via `app.state`.
- Enforce FK existence on create/update; 404 for missing type/station; 404 on unknown vehicle id.
- Expose `available: bool` on reads (`parked_station_id IS NOT NULL`).

**Non-Goals:**

- Rental checkout/return, seed scripts, map aggregates, list query filters.
- API to set `parked_station_id` to null (Rental).
- Physical labels, plate numbers, or soft-delete.

## Decisions

### Layering

- **API** (`app/api/vehicles.py` + Pydantic schemas) → **service** (`VehicleService`) → **repository** (SQLModel).
- Fleet usage: `SqlFleetUsage` / `SqlStationFleetUsage` (names illustrative) in `app/ports/` or `app/repositories/` taking `Session`; registered in `dependencies.py` as default instead of stubs.

**Alternatives:** Query inside existing services only — rejected; ports keep delete rules decoupled and testable.

### Data model

Table `vehicle`:

| Column | Notes |
|--------|--------|
| `id` | UUID PK |
| `vehicle_type_id` | FK → `vehicle_type.id`, NOT NULL, indexed |
| `parked_station_id` | FK → `station.id`, NULL allowed for Rental/Seed; NOT NULL for rows created via Fleet API |

Alembic `0003_fleet_vehicle` creates table and FKs.

**Alternatives:** Enum `status` instead of nullable station — nullable column is enough for "out" in later slices.

### API shape (prefix `/api/v1`)

| Method | Path | Behavior |
|--------|------|----------|
| POST | `/vehicles` | Body: `vehicle_type_id`, `station_id` (parked) → 201 |
| GET | `/vehicles` | List all |
| GET | `/vehicles/{id}` | 200 or 404 |
| PATCH | `/vehicles/{id}` | Partial `vehicle_type_id` and/or `station_id`; empty body → 422 |
| DELETE | `/vehicles/{id}` | 204 or 404 |

JSON uses `station_id` on input for parked station (consistent with operator mental model); responses include `vehicle_type_id`, `station_id` (parked), and `available`.

Missing type/station on create/PATCH → **404**. Invalid UUID / empty PATCH → **422**.

### Availability

- `available = (parked_station_id is not None)`.
- All Fleet API-managed rows have `available: true` until Rental clears parking.

### Capacity gate

- Service does **not** compare parked count to `station.capacity` on create or PATCH.

### Fleet usage port wiring

- `is_type_in_use`: `EXISTS` vehicle with `vehicle_type_id`.
- `has_vehicles_at_station`: `EXISTS` vehicle with `parked_station_id = station_id`.
- Default app wiring uses SQL implementations; `set_*_for_tests(None)` restores SQL after tests; fakes still used where scenarios isolate port behavior.

**Alternatives:** Direct FK-only on delete — ports already specified in vehicle-types and stations specs.

### Testing

- One pytest module per requirement area (add, list, get, patch, delete, capacity-not-gate, availability, type-delete integration, station-delete integration).
- Reuse `conftest` helpers to create type + station + vehicle.
- Add migration test assertion for `vehicle` table after `0003`.
- Run full suite in Docker PostgreSQL after each task group.

## Risks / Trade-offs

- **[Risk]** Rows with null `parked_station_id` inserted only via future Rental could be invisible to Fleet list semantics if filtered — **Mitigation**: list all vehicles; document in Rental.
- **[Risk]** Integration tests for delete today use fakes — **Mitigation**: add fleet spec scenarios with real vehicles; keep fakes for isolated port unit tests.
- **[Risk]** Cyclic imports session in ports — **Mitigation**: thin repository queries inside port classes constructed per request with `Session`.

## Migration Plan

- `alembic upgrade head` on deploy (Docker entrypoint).
- Downgrade drops `vehicle` table per revision downgrade.
- Greenfield: no data backfill.

## Open Questions

- None blocking; optional `GET /vehicles?station_id=` deferred to map capability.
