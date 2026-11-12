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
def test_checkout_rental_posts_vehicle_id() -> None:
  route = respx.post("http://localhost:8000/api/v1/rentals/checkout").mock(
    return_value=httpx.Response(
      201,
      json={
        "id": "r1",
        "vehicle_id": "v1",
        "checkout_station_id": "s1",
        "return_station_id": None,
        "rate_at_checkout": "150",
        "started_at": "2026-01-01T12:00:00Z",
        "ended_at": None,
        "amount_owed": None,
        "paid": False,
      },
    ),
  )
  payload = json.loads(tools.checkout_rental("v1"))
  assert payload["vehicle_id"] == "v1"
  assert route.called
  assert route.calls.last.request.content
  body = json.loads(route.calls.last.request.content)
  assert body["vehicle_id"] == "v1"


@respx.mock
def test_return_rental_posts_station_id() -> None:
  route = respx.post("http://localhost:8000/api/v1/rentals/r1/return").mock(
    return_value=httpx.Response(
      200,
      json={
        "id": "r1",
        "vehicle_id": "v1",
        "checkout_station_id": "s1",
        "return_station_id": "s1",
        "rate_at_checkout": "150",
        "started_at": "2026-01-01T12:00:00Z",
        "ended_at": "2026-01-01T13:00:00Z",
        "amount_owed": "300",
        "paid": False,
      },
    ),
  )
  payload = json.loads(tools.return_rental("r1", "s1"))
  assert payload["return_station_id"] == "s1"
  assert route.called


@respx.mock
def test_record_rental_payment() -> None:
  respx.post("http://localhost:8000/api/v1/rentals/r2/record-payment").mock(
    return_value=httpx.Response(
      200,
      json={
        "id": "r2",
        "vehicle_id": "v1",
        "checkout_station_id": "s1",
        "return_station_id": "s1",
        "rate_at_checkout": "150",
        "started_at": "2026-01-01T12:00:00Z",
        "ended_at": "2026-01-01T13:00:00Z",
        "amount_owed": "300",
        "paid": True,
      },
    ),
  )
  payload = json.loads(tools.record_rental_payment("r2"))
  assert payload["paid"] is True
