import json

import httpx
import pytest
import respx

from greenwheels_mcp import tools


@pytest.fixture(autouse=True)
def reset_client() -> None:
  tools.set_client(None)
  yield
  tools.set_client(None)


@respx.mock
def test_list_stations_tool_returns_names() -> None:
  respx.get("http://localhost:8000/api/v1/stations").mock(
    return_value=httpx.Response(
      200,
      json=[
        {"id": "s1", "name": "Centro", "capacity": 20, "latitude": "-37.32", "longitude": "-59.13"},
        {"id": "s2", "name": "Plaza Independencia", "capacity": 15, "latitude": "-37.32", "longitude": "-59.12"},
      ],
    ),
  )
  payload = json.loads(tools.list_stations())
  names = {s["name"] for s in payload}
  assert names == {"Centro", "Plaza Independencia"}
