"""Scenario: List after one add."""


def test_list_after_one_add(client):
    create = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Monopatín", "current_rate": "220"},
    )
    assert create.status_code == 201

    response = client.get("/api/v1/vehicle-types")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["name"] == "Monopatín"
    rate = items[0]["current_rate"]
    assert rate in ("220", "220.00")
