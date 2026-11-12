from abc import ABC, abstractmethod
from uuid import UUID

from sqlmodel import Session, select

from app.models.vehicle import Vehicle


class FleetUsagePort(ABC):
    @abstractmethod
    def is_type_in_use(self, type_id: UUID) -> bool:
        ...


class StubFleetUsage(FleetUsagePort):
    def is_type_in_use(self, type_id: UUID) -> bool:
        return False


class SqlFleetUsage(FleetUsagePort):
    def __init__(self, session: Session) -> None:
        self._session = session

    def is_type_in_use(self, type_id: UUID) -> bool:
        statement = select(Vehicle).where(Vehicle.vehicle_type_id == type_id).limit(1)
        return self._session.exec(statement).first() is not None
