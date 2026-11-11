from abc import ABC, abstractmethod
from uuid import UUID


class FleetUsagePort(ABC):
    @abstractmethod
    def is_type_in_use(self, type_id: UUID) -> bool:
        ...


class StubFleetUsage(FleetUsagePort):
    def is_type_in_use(self, type_id: UUID) -> bool:
        return False
