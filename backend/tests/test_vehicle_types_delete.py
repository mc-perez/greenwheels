"""Scenarios: delete when unused; delete refused when fleet reports usage."""

from uuid import UUID

from app.main import set_fleet_usage_port_for_tests
from tests.conftest import FakeFleetInUse


def test_delete_when_fleet_reports_no_usage(client):
    created = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "150"},
    )
    type_id = created.json()["id"]

    delete = client.delete(f"/api/v1/vehicle-types/{type_id}")
    assert delete.status_code == 204

    listing = client.get("/api/v1/vehicle-types")
    assert listing.json() == []


def test_delete_refused_when_fleet_reports_usage(client):
    created = client.post(
        "/api/v1/vehicle-types",
        json={"name": "Bici urbana", "current_rate": "150"},
    )
    body = created.json()
    type_id = UUID(body["id"])

    set_fleet_usage_port_for_tests(FakeFleetInUse({type_id}))

    delete = client.delete(f"/api/v1/vehicle-types/{type_id}")
    assert delete.status_code == 409

    listing = client.get("/api/v1/vehicle-types")
    assert len(listing.json()) == 1
    item = listing.json()[0]
    assert item["name"] == "Bici urbana"
    rate = item["current_rate"]
    assert rate in ("150", "150.00")
