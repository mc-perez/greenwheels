import random
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from sqlmodel import Session

from app.models.rental import Rental
from app.models.station import Station
from app.models.vehicle import Vehicle
from app.models.vehicle_type import VehicleType
from app.repositories.rentals import RentalRepository
from app.repositories.stations import StationRepository
from app.repositories.vehicle_types import VehicleTypeRepository
from app.repositories.vehicles import VehicleRepository
from app.seed.empty import database_is_seedable
from app.seed.tandil_landmarks import DEMO_VEHICLE_TYPE_RATES, TANDIL_LANDMARKS
from app.services.rentals import utc_now

SEED_RNG = 42
SEED_VEHICLE_COUNT = 50
SEED_OPEN_RENTAL_COUNT = 5


def seed_vehicle_id(index: int) -> UUID:
    return UUID(f"00000000-0000-4000-8000-{index:012x}")


class SeedDatabaseNotEmptyError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class SeedResult:
    stations: int
    vehicle_types: int
    vehicles: int
    open_rentals: int


class SeedService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._stations = StationRepository(session)
        self._types = VehicleTypeRepository(session)
        self._vehicles = VehicleRepository(session)
        self._rentals = RentalRepository(session)

    def run(self) -> SeedResult:
        if not database_is_seedable(self._session):
            raise SeedDatabaseNotEmptyError()

        rng = random.Random(SEED_RNG)
        types = self._ensure_demo_types()
        stations = self._create_landmark_stations()
        vehicles = self._create_vehicles(rng, types, stations)
        open_count = self._create_open_rentals(rng, vehicles, types)

        return SeedResult(
            stations=len(stations),
            vehicle_types=len(types),
            vehicles=len(vehicles),
            open_rentals=open_count,
        )

    def _ensure_demo_types(self) -> list[VehicleType]:
        existing = self._types.list_all()
        if existing:
            return existing
        created: list[VehicleType] = []
        for name, rate in DEMO_VEHICLE_TYPE_RATES:
            entity = VehicleType(name=name, current_rate=Decimal(rate))
            created.append(self._types.create(entity))
        return created

    def _create_landmark_stations(self) -> list[Station]:
        created: list[Station] = []
        for landmark in TANDIL_LANDMARKS:
            entity = Station(
                name=landmark.name,
                capacity=landmark.capacity,
                latitude=landmark.latitude,
                longitude=landmark.longitude,
            )
            created.append(self._stations.create(entity))
        return created

    def _create_vehicles(
        self,
        rng: random.Random,
        types: list[VehicleType],
        stations: list[Station],
    ) -> list[Vehicle]:
        created: list[Vehicle] = []
        for index in range(SEED_VEHICLE_COUNT):
            vehicle_type = rng.choice(types)
            station = rng.choice(stations)
            entity = Vehicle(
                id=seed_vehicle_id(index),
                vehicle_type_id=vehicle_type.id,
                parked_station_id=station.id,
            )
            created.append(self._vehicles.create(entity))
        return created

    def _create_open_rentals(
        self,
        rng: random.Random,
        vehicles: list[Vehicle],
        types: list[VehicleType],
    ) -> int:
        type_by_id = {t.id: t for t in types}
        indices = sorted(rng.sample(range(SEED_VEHICLE_COUNT), SEED_OPEN_RENTAL_COUNT))
        for index in indices:
            vehicle = vehicles[index]
            vehicle_type = type_by_id[vehicle.vehicle_type_id]
            checkout_station_id = vehicle.parked_station_id
            assert checkout_station_id is not None
            started_at = utc_now() - timedelta(hours=rng.randint(1, 48))
            rental = Rental(
                vehicle_id=vehicle.id,
                checkout_station_id=checkout_station_id,
                rate_at_checkout=vehicle_type.current_rate,
                started_at=started_at,
            )
            vehicle.parked_station_id = None
            self._vehicles.save(vehicle)
            self._rentals.create(rental)
        return len(indices)
