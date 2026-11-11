def test_empty_station_name_rejected(client):
    response = client.post(
        "/api/v1/stations",
        json={
            "name": "",
            "capacity": 10,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    )
    assert response.status_code == 422


def test_capacity_below_one_rejected(client):
    response = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 0,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    )
    assert response.status_code == 422


def test_invalid_earth_latitude_rejected(client):
    response = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 10,
            "latitude": "95",
            "longitude": "-59.13316",
        },
    )
    assert response.status_code == 422


def test_invalid_earth_longitude_rejected(client):
    response = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 10,
            "latitude": "-37.32167",
            "longitude": "200",
        },
    )
    assert response.status_code == 422
