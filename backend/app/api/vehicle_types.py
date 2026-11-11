from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_vehicle_type_service
from app.schemas.vehicle_type import (
    VehicleTypeCreate,
    VehicleTypeRead,
    VehicleTypeUpdate,
)
from app.services.vehicle_types import VehicleTypeInUseError, VehicleTypeService

router = APIRouter(prefix="/vehicle-types", tags=["vehicle-types"])


@router.post("", response_model=VehicleTypeRead, status_code=status.HTTP_201_CREATED)
def create_vehicle_type(
    body: VehicleTypeCreate,
    service: Annotated[VehicleTypeService, Depends(get_vehicle_type_service)],
) -> VehicleTypeRead:
    created = service.create(body.name, body.current_rate)
    return VehicleTypeRead.model_validate(created)


@router.get("", response_model=list[VehicleTypeRead])
def list_vehicle_types(
    service: Annotated[VehicleTypeService, Depends(get_vehicle_type_service)],
) -> list[VehicleTypeRead]:
    items = service.list_all()
    return [VehicleTypeRead.model_validate(item) for item in items]


@router.get("/{type_id}", response_model=VehicleTypeRead)
def get_vehicle_type(
    type_id: UUID,
    service: Annotated[VehicleTypeService, Depends(get_vehicle_type_service)],
) -> VehicleTypeRead:
    entity = service.get(type_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return VehicleTypeRead.model_validate(entity)


@router.patch("/{type_id}", response_model=VehicleTypeRead)
def update_vehicle_type(
    type_id: UUID,
    body: VehicleTypeUpdate,
    service: Annotated[VehicleTypeService, Depends(get_vehicle_type_service)],
) -> VehicleTypeRead:
    if body.name is None and body.current_rate is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one of name or current_rate is required",
        )
    updated = service.update(
        type_id,
        name=body.name,
        current_rate=body.current_rate,
    )
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return VehicleTypeRead.model_validate(updated)


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle_type(
    type_id: UUID,
    service: Annotated[VehicleTypeService, Depends(get_vehicle_type_service)],
) -> Response:
    try:
        deleted = service.delete(type_id)
    except VehicleTypeInUseError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle type is in use by the fleet",
        ) from None
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
