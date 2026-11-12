from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class VehicleCreate(BaseModel):
    vehicle_type_id: UUID
    station_id: UUID


class VehicleUpdate(BaseModel):
    vehicle_type_id: UUID | None = None
    station_id: UUID | None = None

    @model_validator(mode="after")
    def at_least_one_field(self) -> "VehicleUpdate":
        if self.vehicle_type_id is None and self.station_id is None:
            raise ValueError("At least one of vehicle_type_id or station_id is required")
        return self


class VehicleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vehicle_type_id: UUID
    station_id: UUID | None
    available: bool

    @classmethod
    def from_entity(cls, entity: object) -> "VehicleRead":
        parked = getattr(entity, "parked_station_id", None)
        return cls(
            id=getattr(entity, "id"),
            vehicle_type_id=getattr(entity, "vehicle_type_id"),
            station_id=parked,
            available=parked is not None,
        )
