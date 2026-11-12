"""Scenario: List after one add."""

from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_list_after_one_add(client):
    vtype = create_type_via_api(client, "Monopatín", 220)
    station = create_station_via_api(
        client,
        name="Plaza",
        capacity=15,
        latitude="-37.32120",
        longitude="-59.13250",
    )
    created = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )

    listing = client.get("/api/v1/vehicles")
    assert listing.status_code == 200
    items = listing.json()
    assert len(items) == 1
    item = items[0]
    assert item["id"] == created["id"]
    assert item["vehicle_type_id"] == vtype["id"]
    assert item["station_id"] == station["id"]
    assert item["available"] is True
