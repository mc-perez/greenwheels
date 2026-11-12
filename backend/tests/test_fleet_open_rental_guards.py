"""Fleet patch/delete refused while rental is open."""

from tests.conftest import (
    checkout_via_api,
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_patch_refused_while_rental_is_open(client):
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
    checkout_via_api(client, vehicle_id=vehicle["id"])

    patch = client.patch(
        f"/api/v1/vehicles/{vehicle['id']}",
        json={"station_id": station["id"]},
    )
    assert patch.status_code == 409


def test_delete_refused_while_rental_is_open(client):
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
    checkout_via_api(client, vehicle_id=vehicle["id"])

    delete = client.delete(f"/api/v1/vehicles/{vehicle['id']}")
    assert delete.status_code == 409
    assert len(client.get("/api/v1/vehicles").json()) == 1
