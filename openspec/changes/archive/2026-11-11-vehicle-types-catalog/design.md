# Design

## Context

Greenfield repository: no application code yet. See `proposal.md` for motivation. The operator interacts via HTTP API only; there is no UI in this slice. Stack is fixed in `openspec/config.yaml` (FastAPI, SQLModel, PostgreSQL, Docker, pytest).

## Goals / Non-Goals

**Goals:**

- Persist vehicle types (id, name, current rate).
- Implement CRUD-style API: create, list, get by id, rename (patch name), update rate, delete.
- Enforce delete guard via a small **fleet usage port** the domain calls; default implementation reports "no vehicles" until the fleet capability wires a real check.
- Lay down backend package layout, DB session, migrations or create-all for dev, Docker Compose, and pytest with HTTP client tests against the API.

**Non-Goals:**

- React frontend, OpenAPI consumer beyond auto-generated docs.
- Vehicle, station, or rental tables.
- Auth middleware, rate history, or audit log.

## Decisions

### Layering

- **API** (FastAPI routers + Pydantic request/response models) → **service** (vehicle type rules) → **repository** (SQLModel queries).
- Delete calls `FleetUsagePort.is_type_in_use(type_id) -> bool` before removing the row.

**Alternatives:** Put delete rule only in DB foreign key — rejected for this slice because fleet table does not exist yet; port keeps the rule in one place and is testable with a fake.

### Data model

- Table `vehicle_type`: `id` (UUID or serial), `name` (string, non-empty), `current_rate` (numeric, non-negative). No rate history table in v1.

**Alternatives:** Separate `rate_history` — deferred; rental copies rate at checkout per constitution.

### API shape (prefix `/api/v1`)

| Method | Path | Behavior |
|--------|------|----------|
| POST | `/vehicle-types` | Body: `{ "name", "current_rate" }` → 201 + resource |
| GET | `/vehicle-types` | List all |
| GET | `/vehicle-types/{id}` | Single or 404 |
| PATCH | `/vehicle-types/{id}` | `name` and/or `current_rate` (partial) |
| DELETE | `/vehicle-types/{id}` | 204 if unused; 409 if fleet reports in use; 404 if missing |

JSON field `current_rate` is a number; semantics of currency/unit are product pending decisions, not encoded here.

### Fleet usage port (stub)

- Interface in domain layer; **StubFleetUsage** always returns `False` in production wiring for this change.
- Tests for "delete refused" inject a test double that returns `True` for a given type id.

**Alternatives:** Skip refuse-delete tests until fleet — rejected; spec requires the behavior; stub + fake satisfies test-first without fleet tables.

### Persistence and runtime

- SQLModel + PostgreSQL; connection via env in Docker Compose.
- FastAPI app factory; Alembic optional — for minimal first slice, `create_all` on startup in dev/test is acceptable if documented in tasks; prefer Alembic if quick to add.

### Testing

- pytest + `httpx.AsyncClient` (or Starlette TestClient) against app with test database (Postgres in Compose or sqlite if SQLModel allows — prefer same Postgres in CI container).
- One test module per requirement scenario; mark integration vs unit for port fakes.

## Risks / Trade-offs

- **[Risk]** Stub fleet allows delete in production even if fleet data existed elsewhere → **Mitigation**: replace stub with real query in fleet change; single wiring point.
- **[Risk]** Duplicate type names allowed → **Mitigation**: open question; if undesired, add unique constraint in a follow-up without changing rental rules.
- **[Risk]** First change bootstraps a lot of files → **Mitigation**: tasks group scaffolding once, then capability-specific tests.

## Migration Plan

- New Compose stack; empty DB. No data migration.
- Rollback: stop containers and drop volume.

## Open Questions

- Should vehicle type **names** be unique in the catalog?
- **Precision** for `current_rate` (e.g. `Decimal(10,2)` vs integer minor units)?
- **Alembic** from day one vs `create_all` for local dev only?
