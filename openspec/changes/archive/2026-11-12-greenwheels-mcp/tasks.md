# Tasks

## Phase 1 — Package, client, read + rental tools

- [x] 1.1 Add `mcp-server/` package with `pyproject.toml` (`fastmcp`, `httpx` pinned; dev `pytest`, `respx`); verify `pip install -e ".[dev]"` succeeds.
- [x] 1.2 Write pytest **Scenario: Default base URL** for `ApiClient`; verify it fails before `GREENWHEELS_API_URL` handling exists.
- [x] 1.3 Implement `ApiClient` and error formatting; verify default-base-url test passes.
- [x] 1.4 Write pytest for **Scenario: List stations via tool** (mock HTTP); verify fail before `list_stations` tool exists.
- [x] 1.5 Implement `FastMCP` app, stdio entrypoint (`python -m greenwheels_mcp`), Phase 1 read tools (`health_check`, `get_map_stations`, `list_vehicle_types`, `list_stations`, `list_vehicles`, `list_rentals`, `get_rental`); verify list-stations test passes.
- [x] 1.6 Write pytest scenarios for checkout, return, and record payment (spec phase-one rental scenarios); verify fail before rental tools exist.
- [x] 1.7 Implement `checkout_rental`, `return_rental`, `record_rental_payment`; verify rental pytest scenarios pass.
- [x] 1.8 Add README draft “MCP Phase 1” with Cursor `mcpServers` snippet and `.opencode.jsonc.example` with `type: "local"`, `codemode: false`; verify paths document Windows and POSIX venv python.
- [x] 1.9 Manual check: `docker compose up -d api db`, seed if needed, `opencode mcp list` or Cursor tools panel shows server, `list_stations` succeeds.

## Phase 2 — Catalog writes and seed

- [x] 2.1 Write pytest **Scenario: Create vehicle type via tool** and **Scenario: Delete type in use surfaces API error**; verify fail before write tools exist.
- [x] 2.2 Implement `create_vehicle_type`, `update_vehicle_type`, `delete_vehicle_type`; verify type tests pass.
- [x] 2.3 Write pytest for station create validation error scenario; implement `create_station`, `update_station`, `delete_station`; verify tests pass.
- [x] 2.4 Write pytest for vehicle add (reuse fleet API shapes); implement `create_vehicle`, `update_vehicle`, `delete_vehicle`; verify tests pass.
- [x] 2.5 Write pytest **Scenario: Seed empty database via tool** and **Scenario: Seed rejected when network exists**; implement `seed_network` with warning docstring; verify tests pass.
- [x] 2.6 Implement **Scenario: Validation error from station create** in tool error path if not already covered; verify pytest passes.

## Closure — Docs, requirements, regression

- [x] 3.1 Finish README MCP section (full tool table, Phase 1 vs 2, `opencode mcp add` one-liner optional); verify against living API list in README.
- [x] 3.2 Update `requirements.md` with capability **8. MCP operator tools** (stdio, same API rules); verify line aligns with proposal.
- [x] 3.3 Run `pytest -q` in `mcp-server/`; verify all green.
- [x] 3.4 Run `docker compose --profile test run --rm test` from repo root; verify 89+ API tests still pass with no backend edits.

## Workflow follow-up

- Archive with `openspec archive greenwheels-mcp` after Phase 2 manual MCP checks and pytest green.
- Creates `openspec/specs/greenwheels-mcp/spec.md`.
