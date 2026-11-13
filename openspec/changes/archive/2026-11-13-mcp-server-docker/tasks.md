# Tasks

## 1. MCP Docker image

- [x] 1.1 Add `mcp-server/.dockerignore` excluding `.venv`, `*.egg-info`, and `__pycache__`; verify `docker compose build mcp` does not copy venv artifacts into the build context.
- [x] 1.2 Add `mcp-server/Dockerfile` (Python 3.12-slim, install `".[dev]"`, `CMD python -m greenwheels_mcp`); verify **Scenario: Image build succeeds** via `docker compose build mcp`.
- [x] 1.3 Tag image in compose as `greenwheels-mcp` (or equivalent) for reuse by test service; verify `docker compose config` validates.

## 2. Compose wiring

- [x] 2.1 Add `mcp` service to root `docker-compose.yml` with `build: ./mcp-server`, profile `mcp`, `stdin_open: true`, `GREENWHEELS_API_URL=http://api:8000`, `depends_on` api healthy; verify service is absent from `docker compose config --services` without `--profile mcp`.
- [x] 2.2 Add `test-mcp` service (same image, profile `test-mcp`, `command: pytest -q`, working dir `/app` or equivalent per Dockerfile layout); verify **Scenario: MCP pytest in container** via `docker compose --profile test-mcp run --rm test-mcp`.
- [x] 2.3 Run existing `mcp-server` pytest on host (`cd mcp-server && pytest -q`); verify suite still green before and after compose-only edits.

## 3. Documentation and host examples

- [x] 3.1 Update README MCP section with Docker build/run, `docker compose --profile mcp run --rm -i mcp`, venv-vs-Docker table, and Tests row for `test-mcp`; verify documented commands match compose file.
- [x] 3.2 Add `.cursor/mcp.json.docker.example` with `docker compose` args from design; verify JSON parses and paths reference repo-root `docker-compose.yml`.
- [x] 3.3 Update `mcp-server/.opencode.jsonc.example` with optional Docker `command`/`args` block; verify **Scenario: Cursor Docker-backed MCP configuration** and OpenCode venv scenario remain documented.

## 4. Integration and regression

- [x] 4.1 With `docker compose up -d api db`, manual check: `docker compose --profile mcp run --rm -i mcp` and `health_check` or host tool invocation against seeded API; verify **Scenario: Health check from container on Compose network**.
- [x] 4.2 Run `docker compose --profile test run --rm test` from repo root; verify API regression suite unchanged.
- [x] 4.3 Run `openspec validate mcp-server-docker --strict` (or project validate command); verify change artifacts pass validation.

## Workflow follow-up

- Archive with `openspec archive mcp-server-docker` after manual MCP Docker check, `test-mcp` green, and API `test` profile green.
- Sync updates `openspec/specs/greenwheels-mcp/spec.md` with delta requirements.
