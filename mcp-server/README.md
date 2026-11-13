# GreenWheels MCP server

Stdio MCP server that proxies the operator REST API. AI hosts (Cursor, OpenCode, others) spawn this process and call named tools (`list_stations`, `checkout_rental`, etc.).

**You do not** run MCP with `docker compose up mcp`. The host agent starts it on demand (venv Python or `docker compose run -i`).

## Prerequisites

1. [Docker](https://docs.docker.com/get-docker/) with Compose v2.
2. GreenWheels **API and database** running (see [repository README — Getting started](../README.md#getting-started-docker)).
3. Optional but typical: seed the demo network once (`POST /api/v1/seed`) so list/checkout tools return data.

Check the API from your machine:

```bash
curl http://localhost:8000/health
```

Expected: JSON with `"status":"ok"`.

## How it fits together

```text
  OpenCode / Cursor  ----stdio---->  MCP process  ----HTTP---->  API :8000
                                         |
                    GREENWHEELS_API_URL: localhost:8000 (venv)
                    or http://api:8000 (Docker on Compose network)
```

The MCP service never adds business rules; FastAPI validates everything.

## Choose a launch mode

| Mode | When to use | API URL |
|------|-------------|---------|
| **Docker** | No Python on the host, or you want parity with the rest of the stack | `http://api:8000` (set in `docker-compose.yml`) |
| **Host venv** | Fastest cold start while developing MCP itself | `http://localhost:8000` |

---

## Option A — Docker (recommended)

### One-time build

From the **repository root**:

```bash
docker compose build mcp
```

### Smoke test (manual)

With `api` and `db` already up:

```bash
docker compose up -d api db
docker compose --profile mcp run --rm -i mcp
```

The container runs `python -m greenwheels_mcp` and waits on stdin. Press Ctrl+C to exit. That is the same process your agent will attach to.

Verify HTTP from inside the MCP image (optional):

```bash
docker compose --profile mcp run --rm --entrypoint python mcp \
  -c "from greenwheels_mcp.client import ApiClient; print(ApiClient().get('/health'))"
```

### Automated tests (MCP image)

```bash
docker compose --profile test-mcp run --rm test-mcp
```

---

## Option B — Host venv

From `mcp-server/`:

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
$env:GREENWHEELS_API_URL = "http://localhost:8000"
python -m greenwheels_mcp
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export GREENWHEELS_API_URL=http://localhost:8000
python -m greenwheels_mcp
```

Or: `./scripts/run-mcp.sh` (POSIX) after creating the venv.

---

## Configure Cursor

Cursor uses [MCP stdio](https://docs.cursor.com/context/model-context-protocol). Settings live in `.cursor/mcp.json` (user or project).

### Docker-backed MCP

1. Copy [`../.cursor/mcp.json.docker.example`](../.cursor/mcp.json.docker.example) to `.cursor/mcp.json` (or merge the `greenwheels` server block).
2. Set the `-f` argument to the **absolute path** of the repo `docker-compose.yml`.
3. Ensure `docker` is on PATH (or use the full path to `docker.exe` on Windows).
4. Start stack: `docker compose up -d api db` (UI optional).
5. Reload MCP in Cursor; run a tool such as `health_check` or `list_stations`.

### Venv-backed MCP

```json
{
  "mcpServers": {
    "greenwheels": {
      "command": "c:\\path\\to\\greenwheels\\mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["-m", "greenwheels_mcp"],
      "env": {
        "GREENWHEELS_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

Use `.venv/bin/python` on Linux/macOS.

---

## Configure OpenCode

OpenCode reads `opencode.jsonc` at the **repository root** (same level as `docker-compose.yml`).

### Step 1 — Base config

Copy the example and edit paths:

```bash
cp mcp-server/.opencode.jsonc.example opencode.jsonc
```

On Windows, copy in Explorer or:

```powershell
Copy-Item mcp-server\.opencode.jsonc.example opencode.jsonc
```

### Step 2 — Pick a server name

The example defines two entries; enable **one** (or both if you want to switch):

| Key | Launch | Notes |
|-----|--------|--------|
| `greenwheels` | Host venv | Set `command` to your venv Python; `cwd` = `mcp-server` |
| `greenwheels-docker` | Docker | Set `cwd` to repo root; `command` runs `docker compose ... run -i mcp` |

**Docker block (repo root as `cwd`):**

```jsonc
"greenwheels-docker": {
  "type": "local",
  "command": [
    "docker", "compose",
    "-f", "docker-compose.yml",
    "--profile", "mcp",
    "run", "--rm", "-i", "mcp"
  ],
  "cwd": "c:\\code\\greenwheels",
  "codemode": false
}
```

Use your real repo path for `cwd`. On Linux/macOS use forward slashes (e.g. `/home/you/greenwheels`).

**Venv block:**

```jsonc
"greenwheels": {
  "type": "local",
  "command": [".venv/Scripts/python.exe", "-m", "greenwheels_mcp"],
  "cwd": "mcp-server",
  "environment": {
    "GREENWHEELS_API_URL": "http://localhost:8000"
  },
  "codemode": false
}
```

Use `.venv/bin/python` on Linux/macOS.

### Step 3 — CLI alternative (venv only)

```bash
opencode mcp add greenwheels \
  --env GREENWHEELS_API_URL=http://localhost:8000 \
  -- mcp-server/.venv/bin/python -m greenwheels_mcp
```

Adjust the Python path for Windows (`mcp-server/.venv/Scripts/python.exe`).

### Step 4 — Verify

1. `docker compose up -d api db`
2. Seed if needed: `curl -X POST http://localhost:8000/api/v1/seed`
3. From repo root: `opencode mcp list` — `greenwheels` or `greenwheels-docker` should show connected.
4. Invoke `list_stations` in the agent.

Set `"codemode": false` so tools are called directly during bring-up.

---

## Tool reference

Full tool list and REST mapping: [repository README — MCP tools](../README.md#mcp-tools).

---

## Troubleshooting

| Symptom | Check |
|---------|--------|
| `Cannot reach API` | API up? `curl http://localhost:8000/health`. Docker MCP needs `api` healthy before `run mcp`. |
| Empty lists after seed | Run `POST /api/v1/seed` once on an empty DB. |
| Docker MCP fails immediately | `-f` path to `docker-compose.yml` correct? `docker compose build mcp` done? |
| OpenCode cannot find compose file | `cwd` in config must be **repo root** for the Docker server. |
| Cursor MCP red / no tools | Reload window; confirm venv exists or Docker command runs manually. |
| Slow MCP start with Docker | Normal; use venv for faster iteration on MCP code. |
