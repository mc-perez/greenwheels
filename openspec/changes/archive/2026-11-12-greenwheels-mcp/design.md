# Design

## Context

See `proposal.md`. Operator REST API is complete; `operator-console` is a browser client. MCP adds a **stdio child process** both **Cursor** (`mcpServers`) and **OpenCode** (`mcp.servers.*` with `type: "local"`) can spawn with the same command and environment.

## Goals / Non-Goals

**Goals:**

- Package layout: `mcp-server/src/greenwheels_mcp/` (or flat `mcp-server/greenwheels_mcp/`).
- Dependencies: pin `fastmcp` and `httpx`; dev: `pytest`, `respx` (or httpx mock transport).
- `ApiClient`: base URL from env, JSON bodies, map `HTTPStatusError` / FastAPI `detail` to tool errors (string for the agent).
- `server.py`: `FastMCP("greenwheels")`; `@mcp.tool()` per operation; docstrings = operator-facing descriptions.
- Tool return type: **JSON string** (pretty-printed) or structured dict — pick one and use consistently (recommend `str` JSON for uniform agent parsing).
- Phase 1 registers read + rental tools only; Phase 2 adds write tools without renaming Phase 1 tools.
- Docs: `GREENWHEELS_API_URL`, Windows/Linux command arrays, OpenCode `codemode: false` recommended for direct tool calls during bring-up.

**Non-Goals:**

- Streamable HTTP MCP (separate change).
- Sharing `frontend/src/api` with MCP (different language/runtime).
- Running MCP inside the `api` container by default.

## Decisions

### Transport and hosts

- **Choice:** stdio only (`mcp.run()` / `fastmcp run`).
- **Cursor:** `command` + `args` + `env.GREENWHEELS_API_URL`.
- **OpenCode:** `type: "local"`, `command: [...]`, `cwd: "mcp-server"`, `environment: { GREENWHEELS_API_URL: "http://localhost:8000" }`.
- **Alternative:** HTTP remote — deferred; OpenCode supports it but adds deploy complexity.

### Client module

```text
client.get/post/patch/delete(path, json?) -> dict | list
client.format_error(response) -> str
```

Single module; tools are thin wrappers (one HTTP call each).

### Tool naming

Stable snake_case: `list_stations`, `checkout_rental`, `create_vehicle_type`, etc. Prefix domain in name to help tool choice (`rentals_checkout` acceptable alias — pick one convention in Phase 1 and keep it).

### Phase 1 tool set

| Tool | HTTP |
|------|------|
| `health_check` | `GET /health` |
| `get_map_stations` | `GET /api/v1/map/stations` |
| `list_vehicle_types` | `GET /api/v1/vehicle-types` |
| `list_stations` | `GET /api/v1/stations` |
| `list_vehicles` | `GET /api/v1/vehicles` |
| `list_rentals` | `GET /api/v1/rentals` |
| `get_rental` | `GET /api/v1/rentals/{id}` |
| `checkout_rental` | `POST /api/v1/rentals/checkout` `{ vehicle_id }` |
| `return_rental` | `POST /api/v1/rentals/{id}/return` `{ station_id }` |
| `record_rental_payment` | `POST /api/v1/rentals/{id}/record-payment` |

### Phase 2 tool set

CRUD mirrors README API for vehicle-types, stations, vehicles; `seed_network` → `POST /api/v1/seed` with docstring warning (409 when not empty).

### Testing

- **Unit:** `respx` mocks base URL; each scenario from spec asserted on path/method/body.
- **Integration (optional manual):** API via `docker compose up -d api db`, host runs MCP, `opencode mcp list`.
- **Regression:** `docker compose --profile test run --rm test` unchanged after apply.

### Windows vs POSIX

README documents venv python path for both; optional `scripts/run-mcp.ps1` and `scripts/run-mcp.sh` in Phase 1 or 2 to avoid brittle JSON paths.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Too many tools confuse LLM | Phased delivery; clear docstrings; Phase 1 smaller set |
| Agent calls `seed_network` on populated DB | Tool docstring + return 409 message verbatim |
| API down | Connection error as readable tool failure |
| OpenCode Code Mode indirection | Document `codemode: false` in example config |

## Migration Plan

- Install: `cd mcp-server && pip install -e ".[dev]"`.
- Enable in OpenCode/Cursor; verify `list_stations` with seeded DB.
- Rollback: remove MCP config; delete package — API unaffected.

## Open Questions

- Wrapper scripts vs raw venv paths in examples (resolve in Phase 1 tasks if Windows friction appears).
- Whether to pin `fastmcp==` exact version in `pyproject.toml` (recommend yes per FastMCP docs).
