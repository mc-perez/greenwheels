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
def test_create_vehicle_type() -> None:
  route = respx.post("http://localhost:8000/api/v1/vehicle-types").mock(
    return_value=httpx.Response(
      201,
      json={"id": "t1", "name": "Bici urbana", "current_rate": "150"},
    ),
  )
  payload = json.loads(tools.create_vehicle_type("Bici urbana", 150))
  assert payload["name"] == "Bici urbana"
  assert route.called
  body = json.loads(route.calls.last.request.content)
  assert body["name"] == "Bici urbana"
  assert body["current_rate"] == 150


@respx.mock
def test_delete_vehicle_type_in_use_surfaces_error() -> None:
  respx.delete("http://localhost:8000/api/v1/vehicle-types/t1").mock(
    return_value=httpx.Response(409, json={"detail": "Vehicle type in use"}),
  )
  with pytest.raises(RuntimeError, match="Vehicle type in use"):
    tools.delete_vehicle_type("t1")


@respx.mock
def test_create_station_validation_error() -> None:
  respx.post("http://localhost:8000/api/v1/stations").mock(
    return_value=httpx.Response(422, json={"detail": "location outside Tandil urban area"}),
  )
  with pytest.raises(RuntimeError, match="location outside Tandil urban area"):
    tools.create_station("Bad", 5, 0.0, 0.0)


@respx.mock
def test_create_vehicle() -> None:
  route = respx.post("http://localhost:8000/api/v1/vehicles").mock(
    return_value=httpx.Response(
      201,
      json={
        "id": "v1",
        "vehicle_type_id": "t1",
        "station_id": "s1",
        "available": True,
      },
    ),
  )
  payload = json.loads(tools.create_vehicle("t1", "s1"))
  assert payload["available"] is True
  assert route.called


@respx.mock
def test_seed_network_empty_ok() -> None:
  respx.post("http://localhost:8000/api/v1/seed").mock(
    return_value=httpx.Response(201, json={"stations_created": 5}),
  )
  respx.get("http://localhost:8000/api/v1/stations").mock(
    return_value=httpx.Response(
      200,
      json=[{"id": "s1", "name": "Plaza Independencia", "capacity": 10, "latitude": "-37.32", "longitude": "-59.13"}],
    ),
  )
  seed_payload = json.loads(tools.seed_network())
  assert seed_payload["stations_created"] == 5
  stations = json.loads(tools.list_stations())
  assert stations[0]["name"] == "Plaza Independencia"


@respx.mock
def test_seed_network_rejected_when_exists() -> None:
  respx.post("http://localhost:8000/api/v1/seed").mock(
    return_value=httpx.Response(409, json={"detail": "Network already seeded"}),
  )
  with pytest.raises(RuntimeError, match="Network already seeded"):
    tools.seed_network()
