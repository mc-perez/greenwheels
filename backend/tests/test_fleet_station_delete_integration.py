"""Fleet backs station delete usage (real vehicles, no fake port)."""

from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_station_delete_refused_when_a_vehicle_is_parked_there(client):
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vtype = create_type_via_api(client, "Bici urbana", 150)
    create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )

    delete = client.delete(f"/api/v1/stations/{station['id']}")
    assert delete.status_code == 409
    assert len(client.get("/api/v1/stations").json()) == 1


def test_station_delete_succeeds_when_no_vehicle_is_parked_there(client):
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )

    delete = client.delete(f"/api/v1/stations/{station['id']}")
    assert delete.status_code == 204
    assert client.get("/api/v1/stations").json() == []
