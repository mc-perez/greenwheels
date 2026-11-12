"""Payment recording."""

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
T1 = datetime(2026, 6, 1, 12, 1, 0, tzinfo=timezone.utc)
T2 = datetime(2026, 6, 1, 12, 2, 0, tzinfo=timezone.utc)


def test_record_payment_on_closed_rental(client):
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
    with patch("app.services.rentals.utc_now", side_effect=[T0, T1, T2]):
        rental = checkout_via_api(client, vehicle_id=vehicle["id"])
        closed = return_rental_via_api(
            client,
            rental_id=rental["id"],
            station_id=station["id"],
        )

    pay = client.post(f"/api/v1/rentals/{rental['id']}/record-payment")
    assert pay.status_code == 200
    body = pay.json()
    assert body["paid"] is True
    assert body["amount_owed"] == closed["amount_owed"]


def test_reject_payment_before_return(client):
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
    rental = checkout_via_api(client, vehicle_id=vehicle["id"])

    pay = client.post(f"/api/v1/rentals/{rental['id']}/record-payment")
    assert pay.status_code == 409


def test_reject_duplicate_payment(client):
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
    with patch("app.services.rentals.utc_now", side_effect=[T0, T1, T2, T2]):
        rental = checkout_via_api(client, vehicle_id=vehicle["id"])
        return_rental_via_api(client, rental_id=rental["id"], station_id=station["id"])
        assert client.post(f"/api/v1/rentals/{rental['id']}/record-payment").status_code == 200

    again = client.post(f"/api/v1/rentals/{rental['id']}/record-payment")
    assert again.status_code == 409
