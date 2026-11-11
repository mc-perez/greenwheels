"""Scenario: Rate update changes stored current rate."""


def test_rate_update_changes_stored_current_rate(client):
    created = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "150"},
    )
    type_id = created.json()["id"]

    patch = client.patch(
        f"/api/v1/vehicle-types/{type_id}",
        json={"current_rate": "180"},
    )
    assert patch.status_code == 200
    rate = patch.json()["current_rate"]
    assert rate in ("180", "180.00")
