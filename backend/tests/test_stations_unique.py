"""Scenarios: duplicate name on add and rename."""


def test_reject_add_with_duplicate_station_name(client):
    client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 20,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    )
    duplicate = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 10,
            "latitude": "-37.32000",
            "longitude": "-59.13000",
        },
    )
    assert duplicate.status_code == 409
    names = [s["name"] for s in client.get("/api/v1/stations").json()]
    assert names.count("Centro") == 1


def test_reject_rename_to_another_stations_name(client):
    centro = client.post(
        "/api/v1/stations",
        json={
            "name": "Centro",
            "capacity": 20,
            "latitude": "-37.32167",
            "longitude": "-59.13316",
        },
    ).json()
    norte = client.post(
        "/api/v1/stations",
        json={
            "name": "Norte",
            "capacity": 10,
            "latitude": "-37.30000",
            "longitude": "-59.12000",
        },
    ).json()

    conflict = client.patch(
        f"/api/v1/stations/{norte['id']}",
        json={"name": "Centro"},
    )
    assert conflict.status_code == 409

    names = {s["id"]: s["name"] for s in client.get("/api/v1/stations").json()}
    assert names[centro["id"]] == "Centro"
    assert names[norte["id"]] == "Norte"
