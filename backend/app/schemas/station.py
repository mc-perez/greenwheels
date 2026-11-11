from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.geo.tandil import is_inside_tandil_urban


class StationCreate(BaseModel):
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    latitude: Decimal
    longitude: Decimal

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def coerce_decimal(cls, value: object) -> Decimal:
        return Decimal(str(value))

    @field_validator("latitude")
    @classmethod
    def validate_latitude_earth(cls, value: Decimal) -> Decimal:
        if value < -90 or value > 90:
            raise ValueError("latitude out of Earth range")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude_earth(cls, value: Decimal) -> Decimal:
        if value < -180 or value > 180:
            raise ValueError("longitude out of Earth range")
        return value

    @model_validator(mode="after")
    def validate_location_in_tandil(self) -> "StationCreate":
        if not is_inside_tandil_urban(self.latitude, self.longitude):
            raise ValueError("location outside Tandil urban area")
        return self


class StationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    capacity: int | None = Field(default=None, ge=1)
    latitude: Decimal | None = None
    longitude: Decimal | None = None

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def coerce_decimal(cls, value: object) -> Decimal | None:
        if value is None:
            return None
        return Decimal(str(value))

    @field_validator("latitude")
    @classmethod
    def validate_latitude_earth(cls, value: Decimal | None) -> Decimal | None:
        if value is not None and (value < -90 or value > 90):
            raise ValueError("latitude out of Earth range")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude_earth(cls, value: Decimal | None) -> Decimal | None:
        if value is not None and (value < -180 or value > 180):
            raise ValueError("longitude out of Earth range")
        return value

    @model_validator(mode="after")
    def validate_pair_in_tandil_when_both_set(self) -> "StationUpdate":
        if self.latitude is not None and self.longitude is not None:
            if not is_inside_tandil_urban(self.latitude, self.longitude):
                raise ValueError("location outside Tandil urban area")
        return self


class StationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    capacity: int
    latitude: Decimal
    longitude: Decimal
