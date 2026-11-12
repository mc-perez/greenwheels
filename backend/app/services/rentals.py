from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from sqlmodel import Session

from app.billing import compute_amount_owed
from app.models.rental import Rental
from app.models.vehicle import Vehicle
from app.repositories.rentals import RentalRepository
from app.repositories.stations import StationRepository
from app.repositories.vehicle_types import VehicleTypeRepository
from app.repositories.vehicles import VehicleRepository


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class VehicleNotFoundError(Exception):
    pass


class VehicleNotParkedError(Exception):
    pass


class OpenRentalExistsError(Exception):
    pass


class RentalNotFoundError(Exception):
    pass


class RentalNotOpenError(Exception):
    pass


class RentalAlreadyPaidError(Exception):
    pass


class StationNotFoundError(Exception):
    pass


class RentalService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = RentalRepository(session)
        self._vehicles = VehicleRepository(session)
        self._types = VehicleTypeRepository(session)
        self._stations = StationRepository(session)

    def checkout(self, vehicle_id: UUID) -> Rental:
        vehicle = self._vehicles.get(vehicle_id)
        if vehicle is None:
            raise VehicleNotFoundError()
        if vehicle.parked_station_id is None:
            raise VehicleNotParkedError()
        if self._repo.has_open_rental_for_vehicle(vehicle_id):
            raise OpenRentalExistsError()

        vehicle_type = self._types.get(vehicle.vehicle_type_id)
        if vehicle_type is None:
            raise VehicleNotFoundError()

        checkout_station_id = vehicle.parked_station_id
        rental = Rental(
            vehicle_id=vehicle_id,
            checkout_station_id=checkout_station_id,
            rate_at_checkout=vehicle_type.current_rate,
            started_at=utc_now(),
        )
        vehicle.parked_station_id = None
        self._vehicles.save(vehicle)
        return self._repo.create(rental)

    def return_rental(self, rental_id: UUID, station_id: UUID) -> Rental:
        rental = self._repo.get(rental_id)
        if rental is None:
            raise RentalNotFoundError()
        if rental.ended_at is not None:
            raise RentalNotOpenError()
        if self._stations.get(station_id) is None:
            raise StationNotFoundError()

        ended_at = utc_now()
        rental.ended_at = ended_at
        rental.return_station_id = station_id
        rental.amount_owed = compute_amount_owed(
            rental.rate_at_checkout,
            rental.started_at,
            ended_at,
        )

        vehicle = self._vehicles.get(rental.vehicle_id)
        if vehicle is None:
            raise VehicleNotFoundError()
        vehicle.parked_station_id = station_id
        self._vehicles.save(vehicle)
        return self._repo.save(rental)

    def list_all(self) -> list[Rental]:
        return self._repo.list_all()

    def get(self, rental_id: UUID) -> Rental | None:
        return self._repo.get(rental_id)

    def record_payment(self, rental_id: UUID) -> Rental:
        rental = self._repo.get(rental_id)
        if rental is None:
            raise RentalNotFoundError()
        if rental.ended_at is None:
            raise RentalNotOpenError()
        if rental.paid_at is not None:
            raise RentalAlreadyPaidError()
        rental.paid_at = utc_now()
        return self._repo.save(rental)
