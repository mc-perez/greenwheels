# Proposal

## Why

The MCP package already runs on the host via a Python venv, but project constraints require **every component to run locally and in Docker**. Packaging the stdio MCP server as a Compose-backed image closes that gap without changing API business rules or tool contracts, and gives operators a reproducible path that matches `api`, `frontend`, and `db`.

## What Changes

- Add `mcp-server/Dockerfile` and `.dockerignore` following the backend Python image pattern.
- Extend root `docker-compose.yml` with an `mcp` service (Compose profile) that attaches to the stack network, sets `GREENWHEELS_API_URL=http://api:8000`, and supports **interactive stdio** via `docker compose run --rm -i`.
- Add a Compose **test** path for MCP unit tests inside the image (mirroring the existing `test` profile for the API).
- Document **two supported launch modes**: existing host venv (unchanged) and Docker-as-command for Cursor and OpenCode.
- Provide optional example MCP host config snippets that invoke Docker instead of a venv Python path.

## Capabilities

### New Capabilities

<!-- None -->

### Modified Capabilities

- `greenwheels-mcp`: Add requirements for containerized build, Compose wiring, in-container pytest, and documented Docker launch for MCP hosts while keeping stdio transport and existing tools unchanged.

## Functional Requirements Addressed

| Source | RF |
|--------|-----|
| `requirements.md` constraint (all components in Docker) | MCP operator tools run from a published image on the Compose network |
| `requirements.md` capability **8** (MCP operator tools) | Same stdio tools; deployment option documented for Cursor and OpenCode without new API behavior |

Requirements for capabilities **1–7** are unchanged; MCP remains a thin HTTP client to the existing REST API.

## Out of Scope

- Streamable HTTP or SSE MCP transport (separate change).
- Running MCP inside the `api` container or sharing its process.
- New MCP tools, renamed tools, or API/route changes.
- Production hardening (non-root user, image signing, remote registry publish) beyond a dev-focused slim image.
- Automated e2e tests through Cursor or OpenCode UI.
- Replacing or removing host venv workflow (both remain supported).

## Impact

- **New:** `mcp-server/Dockerfile`, `mcp-server/.dockerignore`.
- **Modified:** `docker-compose.yml`, README MCP section, optional `.cursor/mcp.json` / OpenCode example files.
- **Unchanged:** `mcp-server` Python source, FastAPI backend, main `openspec/specs/greenwheels-mcp` tool behaviors (delta adds deployment requirements only).
