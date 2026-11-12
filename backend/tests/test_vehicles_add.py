"""Scenarios: add parked vehicle; reject unknown type or station."""

from uuid import uuid4

from tests.conftest import create_station_via_api, create_type_via_api


def test_add_vehicle_with_type_and_parked_station(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )

    response = client.post(
        "/api/v1/vehicles",
        json={"vehicle_type_id": vtype["id"], "station_id": station["id"]},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["vehicle_type_id"] == vtype["id"]
    assert body["station_id"] == station["id"]
    assert body["available"] is True
    assert "id" in body


def test_reject_add_with_unknown_vehicle_type(client):
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=10,
        latitude="-37.32167",
        longitude="-59.13316",
    )

    response = client.post(
        "/api/v1/vehicles",
        json={"vehicle_type_id": str(uuid4()), "station_id": station["id"]},
    )
    assert response.status_code == 404
    assert client.get("/api/v1/vehicles").json() == []


def test_reject_add_with_unknown_station(client):
    vtype = create_type_via_api(client, "Bici urbana", 150)

    response = client.post(
        "/api/v1/vehicles",
        json={"vehicle_type_id": vtype["id"], "station_id": str(uuid4())},
    )
    assert response.status_code == 404
    assert client.get("/api/v1/vehicles").json() == []
