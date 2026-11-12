"""Scenario: Park when stored capacity is already exceeded."""

from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_park_when_stored_capacity_is_already_exceeded(client):
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=1,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vtype = create_type_via_api(client, "Bici urbana", 150)

    create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )

    second = client.post(
        "/api/v1/vehicles",
        json={"vehicle_type_id": vtype["id"], "station_id": station["id"]},
    )
    assert second.status_code == 201
    assert second.json()["station_id"] == station["id"]

    assert len(client.get("/api/v1/vehicles").json()) == 2
