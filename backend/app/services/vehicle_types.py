from uuid import UUID

from sqlmodel import Session

from app.models.vehicle_type import VehicleType
from app.ports.fleet_usage import FleetUsagePort
from app.repositories.vehicle_types import VehicleTypeRepository


class VehicleTypeInUseError(Exception):
    pass


class VehicleTypeService:
    def __init__(
        self,
        session: Session,
        fleet_usage: FleetUsagePort,
    ) -> None:
        self._repo = VehicleTypeRepository(session)
        self._fleet_usage = fleet_usage

    def create(self, name: str, current_rate) -> VehicleType:
        entity = VehicleType(name=name, current_rate=current_rate)
        return self._repo.create(entity)

    def list_all(self) -> list[VehicleType]:
        return self._repo.list_all()

    def get(self, type_id: UUID) -> VehicleType | None:
        return self._repo.get(type_id)

    def update(
        self,
        type_id: UUID,
        *,
        name: str | None = None,
        current_rate=None,
    ) -> VehicleType | None:
        entity = self._repo.get(type_id)
        if entity is None:
            return None
        if name is not None:
            entity.name = name
        if current_rate is not None:
            entity.current_rate = current_rate
        return self._repo.save(entity)

    def delete(self, type_id: UUID) -> bool:
        entity = self._repo.get(type_id)
        if entity is None:
            return False
        if self._fleet_usage.is_type_in_use(type_id):
            raise VehicleTypeInUseError()
        self._repo.delete(entity)
        return True
