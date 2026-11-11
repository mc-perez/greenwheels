from decimal import Decimal
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class VehicleType(SQLModel, table=True):
    __tablename__ = "vehicle_type"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255, unique=True, index=True)
    current_rate: Decimal = Field(decimal_places=2, max_digits=12, ge=0)
