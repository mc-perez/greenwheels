"""Checkout scenarios."""

from tests.conftest import (
    checkout_via_api,
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_checkout_copies_rate_and_opens_rental(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )

    rental = checkout_via_api(client, vehicle_id=vehicle["id"])
    assert rental["rate_at_checkout"] in ("150", "150.00")
    assert rental["ended_at"] is None

    vehicle_after = client.get(f"/api/v1/vehicles/{vehicle['id']}").json()
    assert vehicle_after["available"] is False
    assert vehicle_after["station_id"] is None


def test_reject_checkout_when_vehicle_already_out(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )
    checkout_via_api(client, vehicle_id=vehicle["id"])

    second = client.post(
        "/api/v1/rentals/checkout",
        json={"vehicle_id": vehicle["id"]},
    )
    assert second.status_code == 409


def test_reject_second_checkout_on_same_vehicle(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )
    checkout_via_api(client, vehicle_id=vehicle["id"])

    assert client.post(
        "/api/v1/rentals/checkout",
        json={"vehicle_id": vehicle["id"]},
    ).status_code == 409
    assert len(client.get("/api/v1/rentals").json()) == 1
