"""List rentals."""

from tests.conftest import (
    checkout_via_api,
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_list_includes_open_rental_after_checkout(client):
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vtype = create_type_via_api(client, "Bici urbana", 150)
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )
    rental = checkout_via_api(client, vehicle_id=vehicle["id"])

    items = client.get("/api/v1/rentals").json()
    assert len(items) == 1
    assert items[0]["id"] == rental["id"]
    assert items[0]["ended_at"] is None
