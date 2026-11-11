from decimal import Decimal
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Station(SQLModel, table=True):
    __tablename__ = "station"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255, unique=True, index=True)
    capacity: int = Field(ge=1)
    latitude: Decimal = Field(decimal_places=6, max_digits=9)
    longitude: Decimal = Field(decimal_places=6, max_digits=9)
