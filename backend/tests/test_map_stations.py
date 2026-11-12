"""Map station list API scenarios from station-map spec."""

from decimal import Decimal

from fastapi.testclient import TestClient

from app.seed.tandil_landmarks import TANDIL_LANDMARKS
from tests.conftest import (
    checkout_via_api,
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
    seed_via_api,
)

MAP_STATIONS_URL = "/api/v1/map/stations"


def _map_stations(client: TestClient) -> list[dict]:
    response = client.get(MAP_STATIONS_URL)
    assert response.status_code == 200
    return response.json()["stations"]


def test_empty_network_returns_no_stations(client: TestClient):
    assert _map_stations(client) == []


def test_seeded_network_returns_five_landmarks(client: TestClient):
    seed_via_api(client)
    stations = _map_stations(client)
    assert len(stations) == 5
    by_name = {item["name"]: item for item in stations}
    assert set(by_name) == {landmark.name for landmark in TANDIL_LANDMARKS}
    for landmark in TANDIL_LANDMARKS:
        item = by_name[landmark.name]
        assert Decimal(str(item["latitude"])) == landmark.latitude
        assert Decimal(str(item["longitude"])) == landmark.longitude
        assert item["capacity"] == landmark.capacity


def test_parked_vehicles_increase_available_count(client: TestClient):
    centro = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    bici = create_type_via_api(client, name="Bici urbana", current_rate=100)
    create_vehicle_via_api(
        client,
        vehicle_type_id=bici["id"],
        station_id=centro["id"],
    )
    create_vehicle_via_api(
        client,
        vehicle_type_id=bici["id"],
        station_id=centro["id"],
    )
    stations = _map_stations(client)
    entry = next(item for item in stations if item["id"] == centro["id"])
    row = next(
        row for row in entry["availability_by_type"] if row["vehicle_type_id"] == bici["id"]
    )
    assert row["available_count"] == 2


def test_vehicle_out_on_open_rental_is_excluded(client: TestClient):
    centro = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    mono = create_type_via_api(client, name="Monopatín", current_rate=200)
    parked = create_vehicle_via_api(
        client,
        vehicle_type_id=mono["id"],
        station_id=centro["id"],
    )
    out = create_vehicle_via_api(
        client,
        vehicle_type_id=mono["id"],
        station_id=centro["id"],
    )
    checkout_via_api(client, vehicle_id=out["id"])
    stations = _map_stations(client)
    entry = next(item for item in stations if item["id"] == centro["id"])
    row = next(
        row for row in entry["availability_by_type"] if row["vehicle_type_name"] == "Monopatín"
    )
    assert row["available_count"] == 1
    assert parked["id"] != out["id"]


def test_missing_type_appears_with_zero(client: TestClient):
    centro = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    bici = create_type_via_api(client, name="Bici urbana", current_rate=100)
    create_type_via_api(client, name="Monopatín", current_rate=200)
    create_vehicle_via_api(
        client,
        vehicle_type_id=bici["id"],
        station_id=centro["id"],
    )
    stations = _map_stations(client)
    entry = next(item for item in stations if item["id"] == centro["id"])
    mono = next(row for row in entry["availability_by_type"] if row["vehicle_type_name"] == "Monopatín")
    assert mono["available_count"] == 0


def test_count_exceeds_stored_capacity(client: TestClient):
    centro = create_station_via_api(
        client,
        name="Centro",
        capacity=1,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    t1 = create_type_via_api(client, name="Bici urbana", current_rate=100)
    t2 = create_type_via_api(client, name="Monopatín", current_rate=200)
    create_vehicle_via_api(client, vehicle_type_id=t1["id"], station_id=centro["id"])
    create_vehicle_via_api(client, vehicle_type_id=t2["id"], station_id=centro["id"])
    stations = _map_stations(client)
    entry = next(item for item in stations if item["id"] == centro["id"])
    assert entry["capacity"] == 1
    total = sum(row["available_count"] for row in entry["availability_by_type"])
    assert total == 2
