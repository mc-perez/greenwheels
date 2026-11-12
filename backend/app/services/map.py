from collections import defaultdict
from uuid import UUID

from sqlmodel import Session

from app.repositories.stations import StationRepository
from app.repositories.vehicle_types import VehicleTypeRepository
from app.repositories.vehicles import VehicleRepository
from app.schemas.map import MapAvailabilityByType, MapStationRead


class MapService:
    def __init__(self, session: Session) -> None:
        self._stations = StationRepository(session)
        self._types = VehicleTypeRepository(session)
        self._vehicles = VehicleRepository(session)

    def list_map_stations(self) -> list[MapStationRead]:
        stations = self._stations.list_all()
        types = sorted(self._types.list_all(), key=lambda t: t.name)
        counts: dict[tuple[UUID, UUID], int] = defaultdict(int)
        for vehicle in self._vehicles.list_all():
            if vehicle.parked_station_id is None:
                continue
            key = (vehicle.parked_station_id, vehicle.vehicle_type_id)
            counts[key] += 1

        result: list[MapStationRead] = []
        for station in stations:
            availability = [
                MapAvailabilityByType(
                    vehicle_type_id=vehicle_type.id,
                    vehicle_type_name=vehicle_type.name,
                    available_count=counts.get((station.id, vehicle_type.id), 0),
                )
                for vehicle_type in types
            ]
            result.append(
                MapStationRead(
                    id=station.id,
                    name=station.name,
                    capacity=station.capacity,
                    latitude=station.latitude,
                    longitude=station.longitude,
                    availability_by_type=availability,
                )
            )
        return result
