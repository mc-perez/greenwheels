"""Scenarios: update capacity; capacity below future occupancy allowed."""


def test_update_capacity_preserves_name_and_location(client):
    created = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 20,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    ).json()
    station_id = created["id"]

    patch = client.patch(
        f"/api/v1/stations/{station_id}",
        json={"capacity": 25},
    )
    assert patch.status_code == 200
    body = patch.json()
    assert body["name"] == "Centro"
    assert body["capacity"] == 25
    assert body["latitude"] in ("-37.321670", "-37.32167")
    assert body["longitude"] in ("-59.133160", "-59.13316")


def test_update_capacity_below_future_occupancy_allowed(client):
    created = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 20,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    ).json()

    patch = client.patch(
        f"/api/v1/stations/{created['id']}",
        json={"capacity": 1},
    )
    assert patch.status_code == 200
    assert patch.json()["capacity"] == 1
