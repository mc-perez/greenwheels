"""Rate snapshot after type update."""

from tests.conftest import (
    checkout_via_api,
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_rate_update_after_checkout_leaves_snapshot(client):
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
    assert rental["rate_at_checkout"] in ("150", "150.00")

    patch = client.patch(
        f"/api/v1/vehicle-types/{vtype['id']}",
        json={"current_rate": "200"},
    )
    assert patch.status_code == 200

    fetched = client.get(f"/api/v1/rentals/{rental['id']}").json()
    assert fetched["rate_at_checkout"] in ("150", "150.00")
