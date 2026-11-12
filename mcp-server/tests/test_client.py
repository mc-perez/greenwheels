import httpx
import pytest
import respx

from greenwheels_mcp.client import ApiClient, GreenwheelsApiError


@respx.mock
def test_default_base_url_uses_localhost_for_stations() -> None:
  route = respx.get("http://localhost:8000/api/v1/stations").mock(
    return_value=httpx.Response(200, json=[]),
  )
  client = ApiClient()
  assert client.get("/api/v1/stations") == []
  assert route.called


@respx.mock
def test_custom_base_url_from_constructor() -> None:
  route = respx.get("http://api.example:9000/health").mock(
    return_value=httpx.Response(200, json={"status": "ok"}),
  )
  client = ApiClient("http://api.example:9000")
  assert client.get("/health") == {"status": "ok"}
  assert route.called


@respx.mock
def test_api_error_includes_detail_string() -> None:
  respx.post("http://localhost:8000/api/v1/stations").mock(
    return_value=httpx.Response(422, json={"detail": "location outside Tandil urban area"}),
  )
  client = ApiClient()
  with pytest.raises(GreenwheelsApiError, match="location outside Tandil urban area"):
    client.post(
      "/api/v1/stations",
      json_body={"name": "X", "capacity": 1, "latitude": 0, "longitude": 0},
    )
