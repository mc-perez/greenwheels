# Design

## Context

See `proposal.md`. The `mcp-server/` package is implemented (FastMCP stdio, httpx client, full tool set). Backend, frontend, and database already run via root `docker-compose.yml`; MCP today is documented only for host venv paths. Project OpenSpec context requires all components in Docker.

## Goals / Non-Goals

**Goals:**

- Reuse the backend Dockerfile pattern (`python:3.12-slim`, install from `pyproject.toml`, `PYTHONUNBUFFERED=1`).
- Add Compose `mcp` service on the default project network with `GREENWHEELS_API_URL=http://api:8000`.
- Keep **stdio** transport: MCP hosts spawn a process; for Docker, the host runs `docker` (or `docker compose run -i`) as the MCP `command`, not a long-lived daemon from plain `docker compose up`.
- Add `test-mcp` (or extend `test` profile) so `pytest -q` runs in the MCP image without a host venv.
- Document venv and Docker paths in README and optional example configs.

**Non-Goals:**

- HTTP/SSE MCP transport.
- Embedding MCP in the `api` image or entrypoint.
- Publishing images to a registry or multi-stage production hardening beyond dev ergonomics.
- Integration tests that require a live MCP host (Cursor/OpenCode) in CI.

## Decisions

### Stdio via `docker compose run -i`, not `up mcp`

- **Choice:** `mcp` service uses profile `mcp`, `stdin_open: true`, `tty: false`, default command `python -m greenwheels_mcp`. Hosts connect with `docker compose --profile mcp run --rm -i mcp`.
- **Rationale:** MCP over stdio needs a single foreground process with stdin/stdout wired to the host. `docker compose up mcp` without `-i` does not attach the host MCP client.
- **Alternative:** Long-running MCP with streamable HTTP — deferred (separate change).

```text
  Cursor / OpenCode
        | spawn: docker compose run -rm -i mcp
        v
  [mcp container] --GREENWHEELS_API_URL--> [api:8000] --> [db]
```

### Service does not join default `up` stack

- **Choice:** Profile `mcp` (and `test-mcp` if split) so `docker compose up -d` stays `db`, `api`, `frontend` only.
- **Rationale:** MCP is on-demand per editor session; no benefit from an idle container.

### Image layout

```text
mcp-server/
  Dockerfile          # COPY pyproject.toml, src/, tests/; pip install ".[dev]"
  .dockerignore       # .venv, __pycache__, egg-info
```

- **CMD:** `["python", "-m", "greenwheels_mcp"]` — same entrypoint as venv.
- **Tests service:** `command: ["pytest", "-q"]`, same image, no stdio flags, profile e.g. `test-mcp`.

Mirror `backend/Dockerfile` structure for consistency; dev dependencies included so in-container pytest matches local `pip install -e ".[dev]"`.

### Host configuration

| Mode | `GREENWHEELS_API_URL` | MCP command |
|------|------------------------|-------------|
| Host venv | `http://localhost:8000` | venv `python -m greenwheels_mcp` |
| Docker (Compose network) | set in compose: `http://api:8000` | `docker compose --profile mcp run --rm -i mcp` |

- **Cursor:** `command`: `docker`, `args`: include `-f` path to repo `docker-compose.yml`, `--profile`, `mcp`, `run`, `--rm`, `-i`, `mcp`. Working directory for compose file must be documented (repo root).
- **Windows:** Document that Docker Desktop provides `docker` on PATH; use absolute path to `docker-compose.yml` in args if Cursor cwd differs.

### Verification beyond unit tests

- **Manual:** With `api` + `db` up, run MCP via Docker and invoke `health_check` or `list_stations` from Cursor/OpenCode.
- **Optional scripted smoke:** Not required in v1 tasks; respx tests stay the automated gate.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Cold start latency per MCP session | Acceptable for dev; document venv path for faster iteration |
| Cursor cwd not repo root | Document `-f` with absolute path to `docker-compose.yml` |
| `docker` not on PATH in GUI apps | README troubleshooting; full path to `docker.exe` on Windows |
| Confusion between `up` and `run -i` | README calls out that MCP hosts use `run -i`, not `up mcp` |

## Migration Plan

- Build: `docker compose build mcp`.
- No API migration or data changes.
- Existing `.cursor/mcp.json` venv config remains valid; operators may switch to Docker example when ready.
- Rollback: remove compose service and Dockerfile; revert docs — venv workflow unchanged.

## Open Questions

- Single profile `test` that runs both API and MCP tests vs separate `test-mcp` profile (default in tasks: separate `test-mcp` mirroring API `test` service for clarity).
- Whether to commit `.cursor/mcp.json.docker.example` vs only README snippets (default: example file without replacing developer-local `mcp.json`).
