"""Scenarios: duplicate vehicle type names on add and rename."""


def test_reject_add_with_duplicate_type_name(client):
    client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "150"},
    )
    duplicate = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "200"},
    )
    assert duplicate.status_code == 409
    types = client.get("/api/v1/vehicle-types").json()
    assert len(types) == 1
    assert types[0]["name"] == "Bici urbana"
    assert types[0]["current_rate"] in ("150", "150.00")


def test_reject_rename_to_another_types_name(client):
    bici = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "150"},
    ).json()
    mono = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Monopatín", "current_rate": "220"},
    ).json()

    conflict = client.patch(
        f"/api/v1/vehicle-types/{mono['id']}",
        json={"name": "Bici urbana"},
    )
    assert conflict.status_code == 409

    names = {t["id"]: t["name"] for t in client.get("/api/v1/vehicle-types").json()}
    assert names[bici["id"]] == "Bici urbana"
    assert names[mono["id"]] == "Monopatín"
