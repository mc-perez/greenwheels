# Proposal

## Why

Vehicle types and stations are in place, but delete guards and future rentals still rely on stub fleet ports. The operator needs persisted vehicles—each linked to a type and parked at a station—before rentals, seed data, or the map can reason about availability.

## What Changes

- Introduce the `vehicle` table and Alembic revision with foreign keys to `vehicle_type` and `station`.
- Expose operator HTTP API under `/api/v1/vehicles` for **parked** vehicles only: create, list, get, partial update (type and/or parked station), and delete.
- Persist `parked_station_id` as nullable in the schema so Rental and Seed can represent vehicles out on a rental later; Fleet API does not create or update vehicles into an "out" state.
- Expose `available` (or equivalent) on reads as true when the vehicle is parked; in this slice that matches every API-managed vehicle.
- Replace `StubFleetUsage` and `StubStationFleetUsage` in default wiring with SQL-backed implementations; existing vehicle-type and station delete scenarios must pass against real data.
- Enforce that parking does not use station capacity as a gate (consistent with stations capability).

## Capabilities

### New Capabilities

- `fleet`: Operator fleet of rental vehicles—each vehicle has one type and is parked at a station when managed through this API; availability is parked; fleet usage ports back station and vehicle-type delete guards.

### Modified Capabilities

<!-- No requirement-level changes to vehicle-types or stations; delete rules already specify fleet port behavior. This change implements those ports. -->

## Functional Requirements Addressed

From `requirements.md` **Capabilities → 3. Fleet**:

| RF | Requirement |
|----|-------------|
| RF-FL-1 | A vehicle has **one vehicle type**. |
| RF-FL-2 | A vehicle is **parked at a station** when added or updated through the operator API in this slice. |
| RF-FL-3 | **Available** means **parked**; API responses SHALL expose that fact for reads. |
| RF-FL-4 | Operator can **add**, **list**, **get**, **update** parked assignment (type and/or station), and **delete** vehicles. |
| RF-FL-5 | **Fleet usage** for existing capabilities: type delete refused while any vehicle references the type; station delete refused while any vehicle is parked at that station. |
| RF-FL-6 | Parking SHALL NOT be rejected because station **capacity** would be exceeded. |

## Out of Scope

- Checkout, return, open rentals, payment, and rental tables (Rental capability).
- Seed of 50 vehicles and vehicles intentionally left "out" without rental API (Seed capability, after Rental).
- Station map UI, availability aggregates by station for the map, and list filters beyond full fleet list (later capabilities).
- Authentication, public client, GPS, hardware docks, and human-readable vehicle labels (plates) beyond system identifier.
- Changing `parked_station_id` to null through Fleet API (reserved for Rental).

## Impact

- New FastAPI router `app/api/vehicles.py`, SQLModel `Vehicle`, repository/service, Pydantic schemas; register on `api_router`.
- Alembic revision `0003_*` creating `vehicle` with FKs; extend `test_database_migrations` if needed.
- `app/ports/fleet_usage.py` and `app/ports/station_fleet_usage.py`: add database-backed implementations; update `dependencies.py` to use them in production (tests keep injectable overrides).
- New pytest modules per fleet spec scenarios; extend integration tests so vehicle-type and station delete refuse paths use real parked vehicles instead of fakes only where scenarios require it.
- README API slice section may be updated during apply to document `/vehicles`.
