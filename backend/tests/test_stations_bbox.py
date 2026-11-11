"""Scenarios: reject latitude south of box; reject longitude west of box."""


def test_reject_latitude_south_of_urban_south_edge(client):
    response = client.post(
        "/api/v1/stations",
        json={
            "name": "Sur inválido",
            "capacity": 10,
            "latitude": "-37.41000",
            "longitude": "-59.13316",
        },
    )
    assert response.status_code == 422
    listing = client.get("/api/v1/stations")
    assert listing.json() == []


def test_reject_longitude_west_of_urban_west_edge(client):
    response = client.post(
        "/api/v1/stations",
        json={
            "name": "Oeste inválido",
            "capacity": 10,
            "latitude": "-37.32167",
            "longitude": "-59.23000",
        },
    )
    assert response.status_code == 422
    listing = client.get("/api/v1/stations")
    assert listing.json() == []
