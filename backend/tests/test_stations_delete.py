"""Scenarios: delete when unused; delete refused when fleet reports usage."""

from uuid import UUID

from app.main import set_station_fleet_usage_port_for_tests
from tests.conftest import FakeStationFleetInUse


def test_delete_when_fleet_reports_no_vehicles_at_station(client):
    created = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 20,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    ).json()

    delete = client.delete(f"/api/v1/stations/{created['id']}")
    assert delete.status_code == 204
    assert client.get("/api/v1/stations").json() == []


def test_delete_refused_when_fleet_reports_usage(client):
    created = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 20,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    ).json()
    station_id = UUID(created["id"])

    set_station_fleet_usage_port_for_tests(FakeStationFleetInUse({station_id}))

    delete = client.delete(f"/api/v1/stations/{created['id']}")
    assert delete.status_code == 409

    items = client.get("/api/v1/stations").json()
    assert len(items) == 1
    assert items[0]["name"] == "Centro"
