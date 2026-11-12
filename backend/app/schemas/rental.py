from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RentalCheckout(BaseModel):
    vehicle_id: UUID


class RentalReturn(BaseModel):
    station_id: UUID


class RentalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vehicle_id: UUID
    checkout_station_id: UUID
    return_station_id: UUID | None
    rate_at_checkout: Decimal
    started_at: datetime
    ended_at: datetime | None
    amount_owed: Decimal | None
    paid: bool

    @classmethod
    def from_entity(cls, entity: object) -> "RentalRead":
        paid_at = getattr(entity, "paid_at", None)
        return cls(
            id=getattr(entity, "id"),
            vehicle_id=getattr(entity, "vehicle_id"),
            checkout_station_id=getattr(entity, "checkout_station_id"),
            return_station_id=getattr(entity, "return_station_id"),
            rate_at_checkout=getattr(entity, "rate_at_checkout"),
            started_at=getattr(entity, "started_at"),
            ended_at=getattr(entity, "ended_at"),
            amount_owed=getattr(entity, "amount_owed"),
            paid=paid_at is not None,
        )
