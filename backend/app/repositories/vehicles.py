from uuid import UUID

from sqlmodel import Session, select

from app.models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, vehicle: Vehicle) -> Vehicle:
        self._session.add(vehicle)
        self._session.flush()
        self._session.refresh(vehicle)
        return vehicle

    def list_all(self) -> list[Vehicle]:
        return list(self._session.exec(select(Vehicle)).all())

    def get(self, vehicle_id: UUID) -> Vehicle | None:
        return self._session.get(Vehicle, vehicle_id)

    def save(self, vehicle: Vehicle) -> Vehicle:
        self._session.add(vehicle)
        self._session.flush()
        self._session.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self._session.delete(vehicle)
        self._session.flush()
