from abc import ABC, abstractmethod
from uuid import UUID


class StationFleetUsagePort(ABC):
    @abstractmethod
    def has_vehicles_at_station(self, station_id: UUID) -> bool:
        ...


class StubStationFleetUsage(StationFleetUsagePort):
    def has_vehicles_at_station(self, station_id: UUID) -> bool:
        return False
