from pydantic import BaseModel


class SeedResultRead(BaseModel):
    stations: int
    vehicle_types: int
    vehicles: int
    open_rentals: int
