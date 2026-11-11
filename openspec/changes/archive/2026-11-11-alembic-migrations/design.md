# Design

## Context

See `proposal.md`. Today `init_db()` calls `create_all` after importing models; Docker Compose runs `uvicorn` directly. Constitution and `openspec/config.yaml` now require Alembic.

## Goals / Non-Goals

**Goals:**

- Alembic project under `backend/alembic/` with `env.py` targeting `SQLModel.metadata`.
- Initial revision `0001` (or similar) creating `vehicle_type` matching `app.models.vehicle_type.VehicleType`.
- Docker `api` (and `test` profile) run `alembic upgrade head` before uvicorn/pytest.
- `init_db()`: no-op or `create_all` **only** when `database_url` starts with `sqlite` (local pytest shortcut).

**Non-Goals:**

- Separate migration microservice.
- Capra layer (stay SQLModel + Alembic).
- Migrating existing prod data (learning project; volume reset documented).

## Decisions

### Layout

```
backend/
  alembic.ini
  alembic/
    env.py
    script.py.mako
    versions/
      xxxx_initial_vehicle_type.py
  scripts/
    entrypoint.sh          # upgrade head, exec uvicorn
```

**Alternatives:** Run migrations from a one-off `migrate` service — rejected for simplicity; entrypoint on `api` is enough for v1.

### env.py

- Read `DATABASE_URL` from the same settings as the app (`app.config.settings`).
- `target_metadata = SQLModel.metadata` after importing `app.models` so all tables register.

### Initial revision

- Hand-written or `alembic revision --autogenerate` once models are imported; review output for UUID and `NUMERIC` types.
- Table name `vehicle_type`, columns `id`, `name`, `current_rate`.

### Startup sequence (Docker)

```text
entrypoint.sh:
  alembic upgrade head
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`test` service/command:

```text
alembic upgrade head && pytest -q
```

### Existing volumes

Developers with old volumes lacking `alembic_version`:

```bash
docker compose down -v   # destructive, dev only
docker compose up -d --build
```

Document in README.

### Local pytest (SQLite)

Unchanged: `conftest` sets `sqlite://`; `init_db` or conftest may still `create_all` for in-memory tests — spec explicitly allows non-Postgres paths.

## Risks / Trade-offs

- **[Risk]** Forgetting to add a revision when adding a model → **Mitigation**: document autogenerate in README; station change must include revision in its tasks.
- **[Risk]** Entrypoint hides migration failures → **Mitigation**: non-zero exit stops container; healthcheck stays failing.

## Migration Plan

1. Ship Alembic + initial revision.
2. Dev reset volume once.
3. Future capabilities append revisions only.

## Open Questions

- Pin Alembic version floor in `pyproject.toml` only, or also cap upper bound?
