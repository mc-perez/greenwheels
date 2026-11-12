from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.seed.tandil_landmarks import TANDIL_LANDMARKS
from app.services.seed import SeedDatabaseNotEmptyError, SeedService, seed_vehicle_id
from tests.conftest import create_station_via_api, seed_via_api

EXPECTED_LANDMARK_NAMES = {landmark.name for landmark in TANDIL_LANDMARKS}
FIRST_VEHICLE_TYPE_NAME = "Bici urbana"
FIRST_VEHICLE_STATION_NAME = "Plaza Independencia"


def test_seed_succeeds_on_empty_database(client: TestClient):
    body = seed_via_api(client)
    assert body == {
        "stations": 5,
        "vehicle_types": 4,
        "vehicles": 50,
        "open_rentals": 5,
    }


def test_seed_rejected_when_network_is_not_empty(client: TestClient):
    create_station_via_api(
        client,
        name="Existing",
        capacity=10,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    stations_before = client.get("/api/v1/stations").json()
    response = client.post("/api/v1/seed")
    assert response.status_code == 409
    assert client.get("/api/v1/stations").json() == stations_before


def test_landmark_stations_are_stored(client: TestClient):
    seed_via_api(client)
    stations = client.get("/api/v1/stations").json()
    names = {s["name"] for s in stations}
    assert names == EXPECTED_LANDMARK_NAMES
    by_name = {s["name"]: s for s in stations}
    for landmark in TANDIL_LANDMARKS:
        stored = by_name[landmark.name]
        assert Decimal(stored["latitude"]) == landmark.latitude
        assert Decimal(stored["longitude"]) == landmark.longitude


def test_demo_types_appear_after_seed(client: TestClient):
    seed_via_api(client)
    types = client.get("/api/v1/vehicle-types").json()
    names = {t["name"] for t in types}
    assert names == {
        "Bici urbana",
        "Monopatín",
        "Bici eléctrica",
        "Moto eléctrica",
    }


def _read_vehicle_index_zero(client: TestClient) -> tuple[str, str]:
    types = {t["id"]: t["name"] for t in client.get("/api/v1/vehicle-types").json()}
    stations = {s["id"]: s["name"] for s in client.get("/api/v1/stations").json()}
    vehicle = client.get(f"/api/v1/vehicles/{seed_vehicle_id(0)}").json()
    return types[vehicle["vehicle_type_id"]], stations[vehicle["station_id"]]


def test_fifty_vehicles_after_seed(client: TestClient):
    seed_via_api(client)
    vehicles = client.get("/api/v1/vehicles").json()
    assert len(vehicles) == 50
    available = sum(1 for v in vehicles if v["available"])
    assert available == 45


def test_seed_assigns_same_type_and_station_to_index_zero_vehicle(client: TestClient):
    seed_via_api(client)
    assignment = _read_vehicle_index_zero(client)
    assert assignment == (FIRST_VEHICLE_TYPE_NAME, FIRST_VEHICLE_STATION_NAME)


def test_open_rentals_reduce_availability(client: TestClient):
    frozen_now = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)
    with patch("app.services.rentals.utc_now", return_value=frozen_now), patch(
        "app.services.seed.utc_now",
        return_value=frozen_now,
    ):
        seed_via_api(client)
    rentals = client.get("/api/v1/rentals").json()
    open_rentals = [r for r in rentals if r["ended_at"] is None]
    assert len(open_rentals) == 5
    vehicles = client.get("/api/v1/vehicles").json()
    assert sum(1 for v in vehicles if not v["available"]) == 5
    for rental in open_rentals:
        assert datetime.fromisoformat(rental["started_at"]) < frozen_now


def test_open_rental_references_a_seeded_station(client: TestClient):
    seed_via_api(client)
    station_ids = {s["id"] for s in client.get("/api/v1/stations").json()}
    rentals = client.get("/api/v1/rentals").json()
    open_rentals = [r for r in rentals if r["ended_at"] is None]
    assert len(open_rentals) == 5
    for rental in open_rentals:
        assert rental["checkout_station_id"] in station_ids


def test_seed_service_raises_when_database_not_empty(session):
    SeedService(session).run()
    with pytest.raises(SeedDatabaseNotEmptyError):
        SeedService(session).run()
