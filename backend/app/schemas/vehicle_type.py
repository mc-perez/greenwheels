from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VehicleTypeCreate(BaseModel):
    name: str = Field(min_length=1)
    current_rate: Decimal = Field(ge=0)


class VehicleTypeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    current_rate: Decimal | None = Field(default=None, ge=0)


class VehicleTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    current_rate: Decimal
