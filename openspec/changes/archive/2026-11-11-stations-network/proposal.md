# Proposal

## Why

GreenWheels needs operator-managed stations before fleet, rentals, seed, or the map can place vehicles, accept returns, or draw markers. Stations are the second capability in the constitution order; they store the urban network's name, capacity, and location constraints for Tandil.

## What Changes

- Introduce persistence and API for operator stations: name, capacity, latitude, and longitude.
- Support create, list, get by id, partial update (name, capacity, and/or location), and delete when no fleet usage is reported at the station.
- Validate coordinates inside the agreed **Tandil urban bounding box** (in addition to valid Earth ranges).
- Enforce **unique station names** across the catalog.
- Expose a **station fleet-usage port** for delete (stub reports "empty" until the fleet capability wires a real check).
- **Modify vehicle types** to require **unique type names** (database constraint + API conflict on create/rename).
- Add Alembic revision(s) for the `station` table, unique indexes on names, and no runtime `create_all` for production schema.

## Capabilities

### New Capabilities

- `stations`: Operator catalog of rental stations — each with a unique name, a capacity stored as fact (not a gate in this capability), and a location inside the Tandil urban bounding box; full CRUD with delete guarded by fleet usage.

### Modified Capabilities

- `vehicle-types`: Add requirement that vehicle type names are unique; reject create or rename that collides with another type's name.

## Functional Requirements Addressed

From `requirements.md` **Capabilities → 2. Stations**:

| RF | Requirement |
|----|-------------|
| RF-ST-1 | A station has a non-empty **unique name**, **capacity** (integer ≥ 1), and **location** inside the Tandil urban area. |
| RF-ST-2 | Operator can **add** a station; the system stores and exposes id, name, capacity, latitude, longitude. |
| RF-ST-3 | Operator can **list** and **get** every station. |
| RF-ST-4 | Operator can **update** name, capacity, and/or location (partial update). |
| RF-ST-5 | Operator can **delete** a station when fleet reports no vehicles at that station; delete is refused when fleet reports usage. |
| RF-ST-6 | **Capacity is a fact, not a gate**: this capability SHALL NOT reject any request because capacity would be exceeded or because parked count exceeds stored capacity. |
| RF-ST-7 | **Geography**: coordinates outside the urban bounding box are rejected. |

From **Capabilities → 1. Vehicle types** (name uniqueness, product decision in this change):

| RF | Requirement |
|----|-------------|
| RF-VT-6 | Vehicle type **names are unique**; create or rename that duplicates another type's name is rejected. |

## Out of Scope

- Authentication, public client, React station map UI, and OpenStreetMap rendering.
- Fleet, rentals, seed data, and payment recording.
- Occupancy checks, return blocking at "full" stations, or using capacity to limit parks/returns (rental/fleet capabilities).
- Proving that seed places are "real" landmarks (seed capability owns concrete coordinates).
- `place_label` / address fields beyond name and coordinates.
- Currency, time zone, and billing units.

## Impact

- New FastAPI router under `/api/v1/stations`, SQLModel `Station` table, repository/service layer mirroring vehicle types.
- New `StationFleetUsagePort` (or equivalent) stub for delete; tests use injectable fakes.
- Alembic migration `0002_*` (and possibly `0003_*` if split) for `station` and unique constraints on `station.name` and `vehicle_type.name`.
- Pydantic validators for urban bbox constants shared by API and tests.
- pytest modules per spec scenario; extend vehicle-type tests for duplicate-name conflicts.
