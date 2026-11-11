# Proposal

## Why

`create_all` on API startup is fragile and cannot evolve the schema safely as stations, fleet, and rentals add tables and constraints. The constitution now requires Alembic before further domain capabilities; this change adopts migrations while the schema still has a single table.

## What Changes

- Add Alembic to the backend with SQLModel metadata wired for autogenerate.
- Add an initial revision creating `vehicle_type` (equivalent to the current model).
- **BREAKING (dev DB):** Existing Docker volumes created only with `create_all` may need a one-time reset or a baseline migration if `alembic_version` is missing.
- Run `alembic upgrade head` before the API serves traffic in Docker (entrypoint or dedicated migrate step).
- Remove PostgreSQL `create_all` from API startup; keep SQLite `create_all` only for optional local pytest without Docker.
- Document migration commands in `README.md`.

## Capabilities

### New Capabilities

- `database-migrations`: Versioned PostgreSQL schema applied through Alembic; API startup in Docker depends on migrations being at head.

### Modified Capabilities

<!-- None in main specs yet; vehicle-types behavior unchanged. -->

## Functional Requirements Addressed

From `requirements.md` **Intent → Constraints**:

| RF | Requirement |
|----|-------------|
| RF-DB-1 | PostgreSQL schema is versioned and applied with Alembic migrations. |
| RF-DB-2 | Runtime does not create or alter production tables with ad-hoc `create_all` when serving the API in Docker. |

## Out of Scope

- Changing vehicle-types API behavior or REST contracts.
- Data migration scripts for production datasets (empty or reset dev volumes is acceptable).
- Squashing or rewriting the initial revision after stations ship (follow-up revisions only).
- Frontend or map work.
- Replacing SQLModel or PostgreSQL.

## Impact

- `backend/pyproject.toml` (alembic dependency).
- `backend/alembic/` (ini, env, versions).
- `backend/app/db.py`, `backend/app/main.py` lifespan.
- `backend/Dockerfile` or entrypoint script; `docker-compose.yml` for test/api startup.
- `README.md` migration section.
