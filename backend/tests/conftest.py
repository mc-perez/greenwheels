import os

# Local pytest without PostgreSQL (Windows, macOS, Linux): share SQLite with the app.
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite://"

from collections.abc import Generator
from decimal import Decimal
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import get_session
from app.migrate import upgrade_head
from app.main import (
    app,
    set_fleet_usage_port_for_tests,
    set_station_fleet_usage_port_for_tests,
)
from app.models.station import Station  # noqa: F401 — register metadata
from app.models.vehicle import Vehicle  # noqa: F401 — register metadata
from app.models.vehicle_type import VehicleType  # noqa: F401 — register metadata
from app.ports.fleet_usage import FleetUsagePort, StubFleetUsage
from app.ports.station_fleet_usage import StationFleetUsagePort


@pytest.fixture(scope="session")
def engine():
    database_url = os.environ["DATABASE_URL"]
    if database_url.startswith("sqlite"):
        eng = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(eng)
        yield eng
        eng.dispose()
        return

    eng = create_engine(database_url)
    SQLModel.metadata.drop_all(eng)
    with eng.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    upgrade_head(database_url)
    try:
        yield eng
    finally:
        SQLModel.metadata.drop_all(eng)
        with eng.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        eng.dispose()


@pytest.fixture(autouse=True)
def _reset_fleet_ports() -> Generator[None, None, None]:
    set_fleet_usage_port_for_tests(None)
    set_station_fleet_usage_port_for_tests(None)
    yield
    set_fleet_usage_port_for_tests(None)
    set_station_fleet_usage_port_for_tests(None)


@pytest.fixture
def session(engine) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    def override_session() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_session] = override_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


class FakeStationFleetInUse(StationFleetUsagePort):
    def __init__(self, in_use_ids: set[UUID] | None = None) -> None:
        self._in_use = in_use_ids or set()

    def has_vehicles_at_station(self, station_id: UUID) -> bool:
        return station_id in self._in_use


@pytest.fixture
def fake_station_fleet_in_use() -> FakeStationFleetInUse:
    return FakeStationFleetInUse()


class FakeFleetInUse(FleetUsagePort):
    def __init__(self, in_use_ids: set[UUID] | None = None) -> None:
        self._in_use = in_use_ids or set()

    def is_type_in_use(self, type_id: UUID) -> bool:
        return type_id in self._in_use


@pytest.fixture
def fake_fleet_in_use() -> FakeFleetInUse:
    return FakeFleetInUse()


def create_type_via_api(
    client: TestClient,
    name: str,
    current_rate: int | Decimal,
) -> dict:
    response = client.post(
        "/api/v1/vehicle-types",
        json={"name": name, "current_rate": str(current_rate)},
    )
    assert response.status_code == 201
    return response.json()


def create_station_via_api(
    client: TestClient,
    *,
    name: str,
    capacity: int,
    latitude: str,
    longitude: str,
) -> dict:
    response = client.post(
        "/api/v1/stations",
        json={
            "name": name,
            "capacity": capacity,
            "latitude": latitude,
            "longitude": longitude,
        },
    )
    assert response.status_code == 201
    return response.json()


def create_vehicle_via_api(
    client: TestClient,
    *,
    vehicle_type_id: str,
    station_id: str,
) -> dict:
    response = client.post(
        "/api/v1/vehicles",
        json={"vehicle_type_id": vehicle_type_id, "station_id": station_id},
    )
    assert response.status_code == 201
    return response.json()
