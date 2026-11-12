from abc import ABC, abstractmethod
from uuid import UUID

from sqlmodel import Session, select

from app.models.vehicle import Vehicle


class StationFleetUsagePort(ABC):
    @abstractmethod
    def has_vehicles_at_station(self, station_id: UUID) -> bool:
        ...


class StubStationFleetUsage(StationFleetUsagePort):
    def has_vehicles_at_station(self, station_id: UUID) -> bool:
        return False


class SqlStationFleetUsage(StationFleetUsagePort):
    def __init__(self, session: Session) -> None:
        self._session = session

    def has_vehicles_at_station(self, station_id: UUID) -> bool:
        statement = (
            select(Vehicle).where(Vehicle.parked_station_id == station_id).limit(1)
        )
        return self._session.exec(statement).first() is not None
