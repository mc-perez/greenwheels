"""Scenarios: update type and/or parked station; reject unknown station."""

from uuid import uuid4

from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_update_parked_station_preserves_type(client):
    bici = create_type_via_api(client, "Bici urbana", 150)
    centro = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    norte = create_station_via_api(
        client,
        name="Norte",
        capacity=10,
        latitude="-37.32000",
        longitude="-59.13000",
    )
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=bici["id"],
        station_id=centro["id"],
    )

    patch = client.patch(
        f"/api/v1/vehicles/{vehicle['id']}",
        json={"station_id": norte["id"]},
    )
    assert patch.status_code == 200
    body = patch.json()
    assert body["vehicle_type_id"] == bici["id"]
    assert body["station_id"] == norte["id"]
    assert body["available"] is True


def test_update_vehicle_type_preserves_parked_station(client):
    bici = create_type_via_api(client, "Bici urbana", 150)
    mono = create_type_via_api(client, "Monopatín", 220)
    centro = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=bici["id"],
        station_id=centro["id"],
    )

    patch = client.patch(
        f"/api/v1/vehicles/{vehicle['id']}",
        json={"vehicle_type_id": mono["id"]},
    )
    assert patch.status_code == 200
    body = patch.json()
    assert body["vehicle_type_id"] == mono["id"]
    assert body["station_id"] == centro["id"]


def test_reject_update_with_unknown_station(client):
    bici = create_type_via_api(client, "Bici urbana", 150)
    centro = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=bici["id"],
        station_id=centro["id"],
    )

    patch = client.patch(
        f"/api/v1/vehicles/{vehicle['id']}",
        json={"station_id": str(uuid4())},
    )
    assert patch.status_code == 404

    unchanged = client.get(f"/api/v1/vehicles/{vehicle['id']}").json()
    assert unchanged["vehicle_type_id"] == bici["id"]
    assert unchanged["station_id"] == centro["id"]
