$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
  Write-Error "Create venv first: cd mcp-server; python -m venv .venv; pip install -e .[dev]"
}
$env:GREENWHEELS_API_URL = if ($env:GREENWHEELS_API_URL) { $env:GREENWHEELS_API_URL } else { "http://localhost:8000" }
& $Python -m greenwheels_mcp
