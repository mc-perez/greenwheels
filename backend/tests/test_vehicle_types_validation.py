def test_empty_name_rejected(client):
    response = client.post(
        "/api/v1/vehicle-types",
        json={"name": "", "current_rate": "10"},
    )
    assert response.status_code == 422


def test_negative_rate_rejected(client):
    response = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Test", "current_rate": "-1"},
    )
    assert response.status_code == 422
