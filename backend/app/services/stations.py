from decimal import Decimal
from uuid import UUID

from sqlmodel import Session

from app.geo.tandil import is_inside_tandil_urban
from app.models.station import Station
from app.ports.station_fleet_usage import StationFleetUsagePort
from app.repositories.stations import StationRepository


class StationInUseError(Exception):
    pass


class StationDuplicateNameError(Exception):
    pass


class StationLocationError(Exception):
    pass


class StationService:
    def __init__(
        self,
        session: Session,
        station_fleet: StationFleetUsagePort,
    ) -> None:
        self._repo = StationRepository(session)
        self._station_fleet = station_fleet

    def create(
        self,
        name: str,
        capacity: int,
        latitude: Decimal,
        longitude: Decimal,
    ) -> Station:
        if self._repo.get_by_name(name) is not None:
            raise StationDuplicateNameError()
        entity = Station(
            name=name,
            capacity=capacity,
            latitude=latitude,
            longitude=longitude,
        )
        return self._repo.create(entity)

    def list_all(self) -> list[Station]:
        return self._repo.list_all()

    def get(self, station_id: UUID) -> Station | None:
        return self._repo.get(station_id)

    def update(
        self,
        station_id: UUID,
        *,
        name: str | None = None,
        capacity: int | None = None,
        latitude: Decimal | None = None,
        longitude: Decimal | None = None,
    ) -> Station | None:
        entity = self._repo.get(station_id)
        if entity is None:
            return None
        if name is not None and name != entity.name:
            existing = self._repo.get_by_name(name)
            if existing is not None and existing.id != entity.id:
                raise StationDuplicateNameError()
            entity.name = name
        if capacity is not None:
            entity.capacity = capacity
        new_lat = latitude if latitude is not None else entity.latitude
        new_lon = longitude if longitude is not None else entity.longitude
        if latitude is not None or longitude is not None:
            if not is_inside_tandil_urban(new_lat, new_lon):
                raise StationLocationError()
            entity.latitude = new_lat
            entity.longitude = new_lon
        return self._repo.save(entity)

    def delete(self, station_id: UUID) -> bool:
        entity = self._repo.get(station_id)
        if entity is None:
            return False
        if self._station_fleet.has_vehicles_at_station(station_id):
            raise StationInUseError()
        self._repo.delete(entity)
        return True
