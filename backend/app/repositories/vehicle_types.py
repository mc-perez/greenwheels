from uuid import UUID

from sqlmodel import Session, select

from app.models.vehicle_type import VehicleType


class VehicleTypeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, vehicle_type: VehicleType) -> VehicleType:
        self._session.add(vehicle_type)
        self._session.flush()
        self._session.refresh(vehicle_type)
        return vehicle_type

    def list_all(self) -> list[VehicleType]:
        return list(self._session.exec(select(VehicleType)).all())

    def get(self, type_id: UUID) -> VehicleType | None:
        return self._session.get(VehicleType, type_id)

    def get_by_name(self, name: str) -> VehicleType | None:
        statement = select(VehicleType).where(VehicleType.name == name)
        return self._session.exec(statement).first()

    def save(self, vehicle_type: VehicleType) -> VehicleType:
        self._session.add(vehicle_type)
        self._session.flush()
        self._session.refresh(vehicle_type)
        return vehicle_type

    def delete(self, vehicle_type: VehicleType) -> None:
        self._session.delete(vehicle_type)
        self._session.flush()
