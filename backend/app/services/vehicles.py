from uuid import UUID

from sqlmodel import Session

from app.models.vehicle import Vehicle
from app.repositories.stations import StationRepository
from app.repositories.vehicle_types import VehicleTypeRepository
from app.repositories.rentals import RentalRepository
from app.repositories.vehicles import VehicleRepository


class VehicleTypeNotFoundError(Exception):
    pass


class VehicleStationNotFoundError(Exception):
    pass


class VehicleOnOpenRentalError(Exception):
    pass


class VehicleService:
    def __init__(self, session: Session) -> None:
        self._repo = VehicleRepository(session)
        self._types = VehicleTypeRepository(session)
        self._stations = StationRepository(session)
        self._rentals = RentalRepository(session)

    def create(self, vehicle_type_id: UUID, station_id: UUID) -> Vehicle:
        self._ensure_type_exists(vehicle_type_id)
        self._ensure_station_exists(station_id)
        entity = Vehicle(
            vehicle_type_id=vehicle_type_id,
            parked_station_id=station_id,
        )
        return self._repo.create(entity)

    def list_all(self) -> list[Vehicle]:
        return self._repo.list_all()

    def get(self, vehicle_id: UUID) -> Vehicle | None:
        return self._repo.get(vehicle_id)

    def update(
        self,
        vehicle_id: UUID,
        *,
        vehicle_type_id: UUID | None = None,
        station_id: UUID | None = None,
    ) -> Vehicle | None:
        entity = self._repo.get(vehicle_id)
        if entity is None:
            return None
        if self._rentals.has_open_rental_for_vehicle(vehicle_id):
            raise VehicleOnOpenRentalError()
        if vehicle_type_id is not None:
            self._ensure_type_exists(vehicle_type_id)
            entity.vehicle_type_id = vehicle_type_id
        if station_id is not None:
            self._ensure_station_exists(station_id)
            entity.parked_station_id = station_id
        return self._repo.save(entity)

    def delete(self, vehicle_id: UUID) -> bool:
        entity = self._repo.get(vehicle_id)
        if entity is None:
            return False
        if self._rentals.has_open_rental_for_vehicle(vehicle_id):
            raise VehicleOnOpenRentalError()
        self._repo.delete(entity)
        return True

    def _ensure_type_exists(self, type_id: UUID) -> None:
        if self._types.get(type_id) is None:
            raise VehicleTypeNotFoundError()

    def _ensure_station_exists(self, station_id: UUID) -> None:
        if self._stations.get(station_id) is None:
            raise VehicleStationNotFoundError()
