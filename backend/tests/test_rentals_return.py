"""Return and amount owed scenarios."""

from datetime import datetime, timezone
from unittest.mock import patch

from tests.conftest import (
    checkout_via_api,
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
    return_rental_via_api,
)

T0 = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
T1 = datetime(2026, 6, 1, 12, 1, 30, tzinfo=timezone.utc)


def test_return_to_full_station_is_allowed(client):
    full = create_station_via_api(
        client,
        name="Centro",
        capacity=1,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    other = create_station_via_api(
        client,
        name="Norte",
        capacity=10,
        latitude="-37.32000",
        longitude="-59.13000",
    )
    vtype = create_type_via_api(client, "Bici urbana", 150)
    create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=full["id"],
    )
    vehicle_out = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=other["id"],
    )

    with patch("app.services.rentals.utc_now", side_effect=[T0, T1]):
        rental = checkout_via_api(client, vehicle_id=vehicle_out["id"])
        closed = return_rental_via_api(
            client,
            rental_id=rental["id"],
            station_id=full["id"],
        )
    assert closed["return_station_id"] == full["id"]

    parked = client.get(f"/api/v1/vehicles/{vehicle_out['id']}").json()
    assert parked["station_id"] == full["id"]
    assert parked["available"] is True


def test_reject_return_on_closed_rental(client):
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vtype = create_type_via_api(client, "Bici urbana", 150)
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )
    with patch("app.services.rentals.utc_now", side_effect=[T0, T1, T1]):
        rental = checkout_via_api(client, vehicle_id=vehicle["id"])
        return_rental_via_api(client, rental_id=rental["id"], station_id=station["id"])

    again = client.post(
        f"/api/v1/rentals/{rental['id']}/return",
        json={"station_id": station["id"]},
    )
    assert again.status_code == 409


def test_ninety_seconds_out_amount_owed_300(client):
    station = create_station_via_api(
        client,
        name="Centro",
        capacity=20,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    vtype = create_type_via_api(client, "Bici urbana", 150)
    vehicle = create_vehicle_via_api(
        client,
        vehicle_type_id=vtype["id"],
        station_id=station["id"],
    )
    with patch("app.services.rentals.utc_now", side_effect=[T0, T1]):
        rental = checkout_via_api(client, vehicle_id=vehicle["id"])
        closed = return_rental_via_api(
            client,
            rental_id=rental["id"],
            station_id=station["id"],
        )
    amount = closed["amount_owed"]
    assert amount in ("300", "300.00")
