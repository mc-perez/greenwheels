from typing import Annotated

from fastapi import Depends, Request
from sqlmodel import Session

from app.db import get_session
from app.ports.fleet_usage import FleetUsagePort, SqlFleetUsage
from app.ports.station_fleet_usage import SqlStationFleetUsage, StationFleetUsagePort
from app.services.rentals import RentalService
from app.services.stations import StationService
from app.services.vehicle_types import VehicleTypeService
from app.services.seed import SeedService
from app.services.vehicles import VehicleService


def get_fleet_usage_port(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> FleetUsagePort:
    override = request.app.state.fleet_usage_port
    if override is not None:
        return override
    return SqlFleetUsage(session)


def get_station_fleet_usage_port(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> StationFleetUsagePort:
    override = request.app.state.station_fleet_usage_port
    if override is not None:
        return override
    return SqlStationFleetUsage(session)


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


def get_vehicle_service(
    session: Annotated[Session, Depends(get_session)],
) -> VehicleService:
    return VehicleService(session)


def get_rental_service(
    session: Annotated[Session, Depends(get_session)],
) -> RentalService:
    return RentalService(session)


def get_seed_service(
    session: Annotated[Session, Depends(get_session)],
) -> SeedService:
    return SeedService(session)
