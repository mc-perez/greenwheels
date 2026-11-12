"""Scenario: Parked vehicle is available on reads."""

from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_parked_vehicle_is_available_on_create_and_get(client):
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
    assert created["available"] is True

    fetched = client.get(f"/api/v1/vehicles/{created['id']}").json()
    assert fetched["available"] is True
