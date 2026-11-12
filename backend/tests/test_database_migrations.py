"""Scenario: Fresh database gets vehicle_type table."""

import os

import pytest
from sqlalchemy import inspect, text
from sqlmodel import SQLModel, create_engine

from app.migrate import upgrade_head

HEAD_REVISION = "0004_rental"


@pytest.mark.skipif(
    os.environ.get("DATABASE_URL", "").startswith("sqlite"),
    reason="PostgreSQL migration test",
)
def test_fresh_database_gets_vehicle_type_table():
    url = os.environ["DATABASE_URL"]
    eng = create_engine(url)
    with eng.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    upgrade_head(url)
    inspector = inspect(eng)
    assert inspector.has_table("vehicle_type")
    columns = {c["name"] for c in inspector.get_columns("vehicle_type")}
    assert columns == {"id", "name", "current_rate"}
    assert inspector.has_table("station")
    station_columns = {c["name"] for c in inspector.get_columns("station")}
    assert station_columns == {"id", "name", "capacity", "latitude", "longitude"}
    with eng.connect() as conn:
        version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
    assert inspector.has_table("vehicle")
    vehicle_columns = {c["name"] for c in inspector.get_columns("vehicle")}
    assert vehicle_columns == {"id", "vehicle_type_id", "parked_station_id"}
    assert inspector.has_table("rental")
    rental_columns = {c["name"] for c in inspector.get_columns("rental")}
    assert rental_columns == {
        "id",
        "vehicle_id",
        "checkout_station_id",
        "return_station_id",
        "rate_at_checkout",
        "started_at",
        "ended_at",
        "amount_owed",
        "paid_at",
    }
    with eng.connect() as conn:
        version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
    assert version == HEAD_REVISION
    eng.dispose()
