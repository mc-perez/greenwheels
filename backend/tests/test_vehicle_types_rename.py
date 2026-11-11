"""Scenario: Rename preserves rate."""


def test_rename_preserves_rate(client):
    created = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "150"},
    )
    type_id = created.json()["id"]

    patch = client.patch(
        f"/api/v1/vehicle-types/{type_id}",
        json={"name": "Bici tradicional"},
    )
    assert patch.status_code == 200
    body = patch.json()
    assert body["name"] == "Bici tradicional"
    rate = body["current_rate"]
    assert rate in ("150", "150.00")
