"""Scenario: Add type with name and rate."""


def test_add_type_with_name_and_rate(client):
    response = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "150"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Bici urbana"
    assert body["current_rate"] == "150.00" or body["current_rate"] == "150"
    assert "id" in body
