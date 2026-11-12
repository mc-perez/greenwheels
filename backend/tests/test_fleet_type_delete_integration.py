"""Fleet backs vehicle type delete usage (real vehicles, no fake port)."""

from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_type_delete_refused_when_a_vehicle_uses_the_type(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )

    delete = client.delete(f"/api/v1/vehicle-types/{vtype['id']}")
    assert delete.status_code == 409
    assert len(client.get("/api/v1/vehicle-types").json()) == 1


def test_type_delete_succeeds_when_no_vehicle_uses_the_type(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)

    delete = client.delete(f"/api/v1/vehicle-types/{vtype['id']}")
    assert delete.status_code == 204
    assert client.get("/api/v1/vehicle-types").json() == []
