from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_station_service
from app.schemas.station import StationCreate, StationRead, StationUpdate
from app.services.stations import (
    StationDuplicateNameError,
    StationInUseError,
    StationLocationError,
    StationService,
)

router = APIRouter(prefix="/stations", tags=["stations"])


@router.post("", response_model=StationRead, status_code=status.HTTP_201_CREATED)
def create_station(
    body: StationCreate,
    service: Annotated[StationService, Depends(get_station_service)],
) -> StationRead:
    try:
        created = service.create(
            body.name,
            body.capacity,
            body.latitude,
            body.longitude,
        )
    except StationDuplicateNameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Station name already exists",
        ) from None
    return StationRead.model_validate(created)


@router.get("", response_model=list[StationRead])
def list_stations(
    service: Annotated[StationService, Depends(get_station_service)],
) -> list[StationRead]:
    items = service.list_all()
    return [StationRead.model_validate(item) for item in items]


@router.get("/{station_id}", response_model=StationRead)
def get_station(
    station_id: UUID,
    service: Annotated[StationService, Depends(get_station_service)],
) -> StationRead:
    entity = service.get(station_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return StationRead.model_validate(entity)


@router.patch("/{station_id}", response_model=StationRead)
def update_station(
    station_id: UUID,
    body: StationUpdate,
    service: Annotated[StationService, Depends(get_station_service)],
) -> StationRead:
    if (
        body.name is None
        and body.capacity is None
        and body.latitude is None
        and body.longitude is None
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one of name, capacity, latitude, or longitude is required",
        )
    try:
        updated = service.update(
            station_id,
            name=body.name,
            capacity=body.capacity,
            latitude=body.latitude,
            longitude=body.longitude,
        )
    except StationDuplicateNameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Station name already exists",
        ) from None
    except StationLocationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="location outside Tandil urban area",
        ) from None
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return StationRead.model_validate(updated)


@router.delete("/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(
    station_id: UUID,
    service: Annotated[StationService, Depends(get_station_service)],
) -> Response:
    try:
        deleted = service.delete(station_id)
    except StationInUseError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Station has vehicles in the fleet",
        ) from None
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
