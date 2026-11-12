from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_map_service
from app.schemas.map import MapStationsResponse
from app.services.map import MapService

router = APIRouter(prefix="/map", tags=["map"])


@router.get("/stations", response_model=MapStationsResponse)
def list_map_stations(
    service: Annotated[MapService, Depends(get_map_service)],
) -> MapStationsResponse:
    stations = service.list_map_stations()
    return MapStationsResponse(stations=stations)
