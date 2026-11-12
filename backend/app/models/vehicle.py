from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Vehicle(SQLModel, table=True):
    __tablename__ = "vehicle"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    vehicle_type_id: UUID = Field(foreign_key="vehicle_type.id", index=True)
    parked_station_id: UUID | None = Field(
        default=None,
        foreign_key="station.id",
        index=True,
    )
