from app.seed.empty import database_is_empty, database_is_seedable
from tests.conftest import (
    create_station_via_api,
    create_type_via_api,
    create_vehicle_via_api,
)


def test_database_is_empty_on_fresh_session(session):
    assert database_is_empty(session)
    assert database_is_seedable(session)


def test_database_is_not_empty_when_station_exists(client, session):
    create_station_via_api(
        client,
        name="Solo",
        capacity=5,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    assert not database_is_empty(session)
    assert not database_is_seedable(session)


def test_database_is_not_empty_when_type_exists(client, session):
    create_type_via_api(client, "Tipo", 100)
    assert not database_is_empty(session)


def test_database_is_not_empty_when_vehicle_exists(client, session):
    t = create_type_via_api(client, "Tipo", 100)
    s = create_station_via_api(
        client,
        name="Solo",
        capacity=5,
        latitude="-37.32167",
        longitude="-59.13316",
    )
    create_vehicle_via_api(client, vehicle_type_id=t["id"], station_id=s["id"])
    assert not database_is_empty(session)
