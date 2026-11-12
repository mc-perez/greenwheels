from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_seed_service
from app.schemas.seed import SeedResultRead
from app.services.seed import SeedDatabaseNotEmptyError, SeedService

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("", response_model=SeedResultRead, status_code=status.HTTP_201_CREATED)
def seed_network(
    service: Annotated[SeedService, Depends(get_seed_service)],
) -> SeedResultRead:
    try:
        result = service.run()
    except SeedDatabaseNotEmptyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database already contains network data",
        ) from None
    return SeedResultRead(
        stations=result.stations,
        vehicle_types=result.vehicle_types,
        vehicles=result.vehicles,
        open_rentals=result.open_rentals,
    )
