# Design

## Context

See `proposal.md` for motivation. The backend already exposes `/api/v1/vehicle-types` with service → repository layering, Alembic revision `0001`, and a `FleetUsagePort` stub for type delete. This change adds stations and tightens name uniqueness for both catalogs.

## Goals / Non-Goals

**Goals:**

- Persist stations (`id`, unique `name`, `capacity`, `latitude`, `longitude`).
- Mirror the vehicle-types API patterns: create, list, get, PATCH, DELETE.
- Validate Earth ranges and the **Tandil urban bounding box** on create and on location update.
- Enforce unique names at API and database level for `station` and `vehicle_type`.
- Delete stations only when `StationFleetUsagePort` reports no vehicles at the station (stub until fleet).
- Ship Alembic revisions; no `create_all` for production schema evolution.

**Non-Goals:**

- Frontend, map, seed, fleet tables, occupancy logic, or bbox download from OSM at runtime.

## Decisions

### Layering

- **API** (`app/api/stations.py` + Pydantic schemas) → **service** (`StationService`, rules + ports) → **repository** (SQLModel).
- Delete calls `StationFleetUsagePort.has_vehicles_at_station(station_id) -> bool` before removing the row.

**Alternatives:** FK-only delete guard — deferred until `vehicle` table exists; port matches vehicle-types.

### Urban bounding box (constants)

Single module (e.g. `app/geo/tandil.py`) with inclusive bounds:

| Bound | Value |
|-------|--------|
| South (min lat) | −37.39785 |
| North (max lat) | −37.25939 |
| West (min lon) | −59.22210 |
| East (max lon) | −59.04832 |

Pydantic field validators on create/update schemas call shared `is_inside_tandil_urban(lat, lon)`.

**Alternatives:** PostGIS polygon — rejected for v1 complexity.

### Data model

- Table `station`: `id` UUID PK, `name` varchar non-empty **UNIQUE**, `capacity` integer `>= 1`, `latitude` / `longitude` as `Numeric` or double with fixed precision in API (recommend `Numeric(9, 6)`).
- Alter `vehicle_type`: **UNIQUE** on `name`.

**Alternatives:** Case-insensitive unique (`citext`) — use case-sensitive UTF-8 unique index unless product asks otherwise.

### API shape (prefix `/api/v1`)

| Method | Path | Behavior |
|--------|------|----------|
| POST | `/stations` | Body: `name`, `capacity`, `latitude`, `longitude` → 201 |
| GET | `/stations` | List all |
| GET | `/stations/{id}` | 200 or 404 |
| PATCH | `/stations/{id}` | Partial `name`, `capacity`, `latitude`, `longitude`; empty body → 422 |
| DELETE | `/stations/{id}` | 204 if unused; 409 if port reports vehicles; 404 if missing |

Conflicts:

- Duplicate `station.name` or `vehicle_type.name` on create/rename → **409** with clear detail.
- Outside bbox or invalid capacity → **422**.

JSON fields: `latitude`, `longitude` (WGS84 degrees).

### Station fleet usage port (stub)

- `StationFleetUsagePort` in `app/ports/`; `StubStationFleetUsage` always returns `False`.
- Tests for delete-refused inject a fake returning `True` for a given `station_id`.

### Vehicle type uniqueness

- Alembic migration adds unique index on `vehicle_type.name`.
- Service checks before insert/rename; rely on DB unique constraint as backstop (`409` on integrity error).
- Extend existing vehicle-type tests with duplicate add/rename scenarios from delta spec.

### Alembic

- Prefer one revision `0002_stations_and_unique_names` creating `station` and unique indexes on both tables, or split `0002` station + `0003` unique on types if cleaner for rollback docs.

### Testing

- One pytest module per requirement area (add, list, get, patch, bbox, unique names, delete, capacity-not-gate).
- Reuse HTTP client + PostgreSQL fixtures from `conftest.py`.
- Bbox tests use coordinates from spec scenarios (valid centro; invalid −37.41 lat, −59.23 lon).

## Risks / Trade-offs

- **[Risk]** Urban bbox may exclude a legitimate partido edge case the operator cares about → **Mitigation**: constants in one module; product already chose urban box.
- **[Risk]** Stub station delete allows removal while fleet data might exist later → **Mitigation**: replace stub in fleet change; single wiring point in dependencies.
- **[Risk]** Unique name migration fails if duplicate rows exist → **Mitigation**: greenfield DB; migration task verifies empty duplicate check before apply.

## Migration Plan

- Run `alembic upgrade head` on deploy (Docker entrypoint already upgrades).
- Rollback: downgrade revision drops `station` and unique constraints per Alembic downgrade.

## Open Questions

- None blocking implementation; case-insensitive names can be a follow-up if needed.
