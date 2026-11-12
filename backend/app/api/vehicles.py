from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.dependencies import get_vehicle_service
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate
from app.services.vehicles import (
    VehicleService,
    VehicleStationNotFoundError,
    VehicleTypeNotFoundError,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    body: VehicleCreate,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
) -> VehicleRead:
    try:
        created = service.create(body.vehicle_type_id, body.station_id)
    except VehicleTypeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle type not found",
        ) from None
    except VehicleStationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station not found",
        ) from None
    return VehicleRead.from_entity(created)


@router.get("", response_model=list[VehicleRead])
def list_vehicles(
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
) -> list[VehicleRead]:
    items = service.list_all()
    return [VehicleRead.from_entity(item) for item in items]


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(
    vehicle_id: UUID,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
) -> VehicleRead:
    entity = service.get(vehicle_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return VehicleRead.from_entity(entity)


@router.patch("/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(
    vehicle_id: UUID,
    body: VehicleUpdate,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
) -> VehicleRead:
    try:
        updated = service.update(
            vehicle_id,
            vehicle_type_id=body.vehicle_type_id,
            station_id=body.station_id,
        )
    except VehicleTypeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle type not found",
        ) from None
    except VehicleStationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station not found",
        ) from None
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return VehicleRead.from_entity(updated)


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: UUID,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
) -> Response:
    deleted = service.delete(vehicle_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
