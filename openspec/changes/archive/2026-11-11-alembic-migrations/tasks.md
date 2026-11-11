# Tasks

## 1. Dependencies and Alembic scaffold

- [x] 1.1 Add `alembic` to `backend/pyproject.toml` and rebuild the Docker image; verify `alembic --version` inside the `api` image.
- [x] 1.2 Run `alembic init` under `backend/`, wire `env.py` to `app.config.settings.database_url` and `SQLModel.metadata` (import `app.models`); verify `alembic current` runs in the container against Postgres.

## 2. Initial revision (RF-DB-1)

- [x] 2.1 Add integration test **Scenario: Fresh database gets vehicle_type table** (assert `alembic_version` at head and table exists after startup helper); verify it fails before the revision exists.
- [x] 2.2 Author revision creating `vehicle_type` matching the SQLModel model; verify the test passes when `alembic upgrade head` is run.

## 3. Startup behavior (RF-DB-2)

- [x] 3.1 Add test **Scenario: No create_all on PostgreSQL startup** (inspect or spy that `create_all` is not called when URL is PostgreSQL); verify it fails while `init_db` still calls `create_all`.
- [x] 3.2 Change `init_db()` to skip `create_all` for PostgreSQL; keep SQLite path for local pytest; verify test passes.
- [x] 3.3 Add `backend/scripts/entrypoint.sh`, update `Dockerfile` CMD to entrypoint running `alembic upgrade head` then uvicorn; verify **Scenario: API accepts writes after migrate** via HTTP test or existing pytest after compose up.

## 4. Docker test profile and docs

- [x] 4.1 Update `test` service to run `alembic upgrade head` before `pytest`; verify `docker compose --profile test run --rm test` passes all tests.
- [x] 4.2 Document `alembic upgrade head`, revision workflow, and `docker compose down -v` reset in `README.md`; verify commands match the implemented entrypoint.

## Workflow follow-up

- Archive with `/opsx-archive` after the suite passes in Docker.
- Archive `vehicle-types-catalog` if not already synced to `openspec/specs/`.
