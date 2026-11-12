from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_rental_service
from app.schemas.rental import RentalCheckout, RentalRead, RentalReturn
from app.services.rentals import (
    OpenRentalExistsError,
    RentalAlreadyPaidError,
    RentalNotFoundError,
    RentalNotOpenError,
    RentalService,
    StationNotFoundError,
    VehicleNotFoundError,
    VehicleNotParkedError,
)

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post("/checkout", response_model=RentalRead, status_code=status.HTTP_201_CREATED)
def checkout(
    body: RentalCheckout,
    service: Annotated[RentalService, Depends(get_rental_service)],
) -> RentalRead:
    try:
        rental = service.checkout(body.vehicle_id)
    except VehicleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found") from None
    except (VehicleNotParkedError, OpenRentalExistsError):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle cannot be checked out",
        ) from None
    return RentalRead.from_entity(rental)


@router.get("", response_model=list[RentalRead])
def list_rentals(
    service: Annotated[RentalService, Depends(get_rental_service)],
) -> list[RentalRead]:
    return [RentalRead.from_entity(r) for r in service.list_all()]


@router.get("/{rental_id}", response_model=RentalRead)
def get_rental(
    rental_id: UUID,
    service: Annotated[RentalService, Depends(get_rental_service)],
) -> RentalRead:
    entity = service.get(rental_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return RentalRead.from_entity(entity)


@router.post("/{rental_id}/return", response_model=RentalRead)
def return_rental(
    rental_id: UUID,
    body: RentalReturn,
    service: Annotated[RentalService, Depends(get_rental_service)],
) -> RentalRead:
    try:
        rental = service.return_rental(rental_id, body.station_id)
    except RentalNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found") from None
    except RentalNotOpenError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rental is not open",
        ) from None
    except StationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found") from None
    return RentalRead.from_entity(rental)


@router.post("/{rental_id}/record-payment", response_model=RentalRead)
def record_payment(
    rental_id: UUID,
    service: Annotated[RentalService, Depends(get_rental_service)],
) -> RentalRead:
    try:
        rental = service.record_payment(rental_id)
    except RentalNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found") from None
    except RentalNotOpenError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rental is still open",
        ) from None
    except RentalAlreadyPaidError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rental already paid",
        ) from None
    return RentalRead.from_entity(rental)
