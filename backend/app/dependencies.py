from typing import Annotated

from fastapi import Depends, Request
from sqlmodel import Session

from app.db import get_session
from app.ports.fleet_usage import FleetUsagePort, StubFleetUsage
from app.services.vehicle_types import VehicleTypeService

_stub_fleet_usage = StubFleetUsage()


def get_fleet_usage_port(request: Request) -> FleetUsagePort:
    override = request.app.state.fleet_usage_port
    if override is not None:
        return override
    return _stub_fleet_usage


def get_vehicle_type_service(
    session: Annotated[Session, Depends(get_session)],
    fleet_usage: Annotated[FleetUsagePort, Depends(get_fleet_usage_port)],
) -> VehicleTypeService:
    return VehicleTypeService(session, fleet_usage)
