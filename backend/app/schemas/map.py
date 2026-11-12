from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MapAvailabilityByType(BaseModel):
    vehicle_type_id: UUID
    vehicle_type_name: str
    available_count: int = Field(ge=0)


class MapStationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    capacity: int
    latitude: Decimal
    longitude: Decimal
    availability_by_type: list[MapAvailabilityByType]


class MapStationsResponse(BaseModel):
    stations: list[MapStationRead]
