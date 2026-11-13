# Spec Delta

## ADDED Requirements

### Requirement: MCP server is published as a Docker image

The project SHALL provide a `Dockerfile` under `mcp-server/` that installs the `greenwheels-mcp` package and uses `python -m greenwheels_mcp` as the container entrypoint.

#### Scenario: Image build succeeds

- **WHEN** an operator runs `docker compose build mcp` from the repository root
- **THEN** the build completes without error
- **AND** the resulting image can run `python -m greenwheels_mcp`

### Requirement: Compose wires MCP to the API on the stack network

The root `docker-compose.yml` SHALL define an `mcp` service built from `mcp-server/`, set `GREENWHEELS_API_URL` to `http://api:8000`, declare a Compose profile so `mcp` does not start on a default `docker compose up`, and enable interactive stdio for host-spawned runs.

#### Scenario: Health check from container on Compose network

- **WHEN** services `db` and `api` are healthy via `docker compose up -d api db`
- **AND** an operator runs `docker compose --profile mcp run --rm -i mcp` with stdin attached and invokes the `health_check` tool
- **THEN** the tool succeeds
- **AND** the HTTP request targets `http://api:8000/health`

### Requirement: MCP unit tests run inside the Docker image

The project SHALL document a Compose command that runs `pytest -q` in `mcp-server/` using the MCP image (for example a `test-mcp` service with a dedicated profile), matching the existing respx-based unit tests without requiring a host venv.

#### Scenario: MCP pytest in container

- **WHEN** an operator runs the documented MCP test Compose command from the repository root
- **THEN** the `mcp-server` pytest suite completes with all tests passing

## MODIFIED Requirements

### Requirement: MCP is documented for Cursor and OpenCode stdio

The project SHALL document local launch for Cursor MCP settings and for OpenCode `mcp.servers` with `type` `local`, using the same entrypoint (`python -m greenwheels_mcp`). The documentation SHALL include both host venv launch and Docker launch via `docker compose --profile mcp run --rm -i mcp`, with `GREENWHEELS_API_URL` set appropriately for each mode (`http://localhost:8000` on the host, `http://api:8000` inside Compose).

#### Scenario: OpenCode local server configuration

- **WHEN** the operator copies the documented `opencode.jsonc` example with `GREENWHEELS_API_URL` `http://localhost:8000`
- **AND** runs `opencode mcp list`
- **THEN** the greenwheels server is shown as connected when the API is reachable

#### Scenario: Cursor Docker-backed MCP configuration

- **WHEN** the operator configures Cursor `mcpServers.greenwheels` with `command` `docker` and documented `args` for `docker compose --profile mcp run --rm -i mcp` from the repository root
- **AND** `docker compose up -d api db` has been run
- **THEN** Cursor can start the greenwheels MCP server
- **AND** `list_stations` succeeds when the network is seeded
