"""Scenario: Get existing vehicle."""

from uuid import uuid4

from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_get_existing_vehicle(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    created = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )

    response = client.get(f"/api/v1/vehicles/{created['id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["vehicle_type_id"] == vtype["id"]
    assert body["station_id"] == station["id"]
    assert body["available"] is True


def test_get_unknown_vehicle_returns_404(client):
    response = client.get(f"/api/v1/vehicles/{uuid4()}")
    assert response.status_code == 404
