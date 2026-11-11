"""Scenario: Get existing station."""


def test_get_existing_station(client):
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

    response = client.get(f"/api/v1/stations/{station_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Centro"
    assert body["capacity"] == 20
    assert "latitude" in body
    assert "longitude" in body


def test_get_unknown_station_returns_404(client):
    response = client.get(
        "/api/v1/stations/00000000-0000-0000-0000-000000000001"
    )
    assert response.status_code == 404
