"""Scenario: List after one add."""


def test_list_after_one_add(client):
    client.post(
        "/api/v1/stations",
        json={
            "name": "Plaza Independencia",
            "capacity": 15,
            "latitude": "-37.32120",
            "longitude": "-59.13250",
        },
    )
    listing = client.get("/api/v1/stations")
    assert listing.status_code == 200
    items = listing.json()
    assert len(items) == 1
    item = items[0]
    assert item["name"] == "Plaza Independencia"
    assert item["capacity"] == 15
