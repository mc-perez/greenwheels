# Proposal

## Why

Agents in **Cursor** and **OpenCode** need the same operator workflows as the React console and Swagger, without a browser. A local **MCP server** that proxies the existing REST API gives a stable tool surface for checkout, catalog edits, and map reads while backend rules stay in FastAPI.

## What Changes

- Add `mcp-server/` Python package: **FastMCP** (stdio), **httpx** client, `GREENWHEELS_API_URL` (default `http://localhost:8000`).
- Expose **named MCP tools** that map to `/api/v1/...` (no business logic in MCP beyond HTTP and error formatting).
- Deliver in **two apply phases inside one change** (see `tasks.md`):
  - **Phase 1:** health, map read, catalog **list** tools, rental **list/get/checkout/return/record-payment**, HTTP client tests, dual-host connection docs (Cursor + OpenCode).
  - **Phase 2:** catalog **create/update/delete** tools, optional `seed_network`, remaining tests and README completion.
- Example configs: `.opencode.jsonc.example`, Cursor MCP snippet in README (no secrets committed).
- **No** FastAPI or Alembic changes in the happy path.

## Capabilities

### New Capabilities

- `greenwheels-mcp`: stdio MCP tools that invoke the operator REST API, documented for Cursor and OpenCode local servers.

### Modified Capabilities

<!-- Backend and operator-console specs unchanged; MCP is another HTTP client. -->

## Functional Requirements Addressed

| Source | RF |
|--------|-----|
| `requirements.md` capabilities **1–5** (operator actions) | Agent invokes the same API as the console for catalogs, fleet, rentals, seed |
| `requirements.md` capability **6** (map) | Agent can read map stations payload |
| New intent (proposed **capability 8** in `requirements.md` at apply/archive) | External MCP hosts may operate the local API via documented tools |

## Implementation phases (single change)

| Phase | Tools (summary) | Agent can… |
|-------|-----------------|------------|
| **1** | `health_check`, `get_map_stations`, `list_*` (types, stations, vehicles, rentals), `get_rental`, `checkout_rental`, `return_rental`, `record_rental_payment` | Run full rental flow on existing data; read network state |
| **2** | `create/update/delete_*` for types, stations, vehicles; `seed_network` | Mutate catalogs and seed an empty DB |

Phase 1 is shippable for manual MCP verification before Phase 2 lands in the same archive.

## Out of Scope

- Authentication, API keys, OAuth on the MCP process, internet-exposed MCP or HTTP transport (follow-up change if needed).
- Generic `raw_http` tool without path allowlist.
- Duplicating validation (Tandil bbox, rental rules) in MCP — only FastAPI validates.
- Playwright, e2e through Cursor/OpenCode UI.
- Auto-refreshing the React map or new BFF endpoints.

## Impact

- **New:** `mcp-server/` (`pyproject.toml`, package, pytest, examples).
- **Docs:** README section “MCP (Cursor & OpenCode)”.
- **Optional:** `requirements.md` capability 8 one-liner when archiving.
- **Docker:** API must be running; MCP typically on **host stdio** (not a required Compose service for v1).
