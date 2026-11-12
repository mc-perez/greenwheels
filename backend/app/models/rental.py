from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class Rental(SQLModel, table=True):
    __tablename__ = "rental"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    vehicle_id: UUID = Field(foreign_key="vehicle.id", index=True)
    checkout_station_id: UUID = Field(foreign_key="station.id")
    return_station_id: UUID | None = Field(default=None, foreign_key="station.id")
    rate_at_checkout: Decimal = Field(decimal_places=2, max_digits=12, ge=0)
    started_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    ended_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    amount_owed: Decimal | None = Field(
        default=None,
        decimal_places=2,
        max_digits=12,
        ge=0,
    )
    paid_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
