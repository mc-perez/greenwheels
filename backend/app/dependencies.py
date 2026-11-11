from typing import Annotated

from fastapi import Depends, Request
from sqlmodel import Session

from app.db import get_session
from app.ports.fleet_usage import FleetUsagePort, StubFleetUsage
from app.ports.station_fleet_usage import StationFleetUsagePort, StubStationFleetUsage
from app.services.stations import StationService
from app.services.vehicle_types import VehicleTypeService

_stub_fleet_usage = StubFleetUsage()
_stub_station_fleet_usage = StubStationFleetUsage()


def get_fleet_usage_port(request: Request) -> FleetUsagePort:
    override = request.app.state.fleet_usage_port
    if override is not None:
        return override
    return _stub_fleet_usage


def get_station_fleet_usage_port(request: Request) -> StationFleetUsagePort:
    override = request.app.state.station_fleet_usage_port
    if override is not None:
        return override
    return _stub_station_fleet_usage


def get_vehicle_type_service(
    session: Annotated[Session, Depends(get_session)],
    fleet_usage: Annotated[FleetUsagePort, Depends(get_fleet_usage_port)],
) -> VehicleTypeService:
    return VehicleTypeService(session, fleet_usage)


def get_station_service(
    session: Annotated[Session, Depends(get_session)],
    station_fleet: Annotated[StationFleetUsagePort, Depends(get_station_fleet_usage_port)],
) -> StationService:
    return StationService(session, station_fleet)
