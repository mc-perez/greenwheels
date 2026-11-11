"""Scenario: Add station with name, capacity, and urban coordinates."""


def test_add_station_with_name_capacity_and_urban_coordinates(client):
    response = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 20,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Centro"
    assert body["capacity"] == 20
    assert body["latitude"] in ("-37.321670", "-37.32167")
    assert body["longitude"] in ("-59.133160", "-59.13316")
    assert "id" in body
