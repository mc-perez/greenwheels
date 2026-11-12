from __future__ import annotations

import json
from typing import Any

from greenwheels_mcp.client import ApiClient, GreenwheelsApiError

_client: ApiClient | None = None


def set_client(client: ApiClient | None) -> None:
    global _client
    _client = client


def get_client() -> ApiClient:
    global _client
    if _client is None:
        _client = ApiClient()
    return _client


def _dump(data: Any) -> str:
    return json.dumps(data, indent=2, default=str)


def _run(callable_fn: Any) -> str:
    try:
        return _dump(callable_fn())
    except GreenwheelsApiError as exc:
        raise RuntimeError(str(exc)) from exc


# --- Phase 1: read + rentals ---


def health_check() -> str:
    return _run(lambda: get_client().get("/health"))


def get_map_stations() -> str:
    return _run(lambda: get_client().get("/api/v1/map/stations"))


def list_vehicle_types() -> str:
    return _run(lambda: get_client().get("/api/v1/vehicle-types"))


def list_stations() -> str:
    return _run(lambda: get_client().get("/api/v1/stations"))


def list_vehicles() -> str:
    return _run(lambda: get_client().get("/api/v1/vehicles"))


def list_rentals() -> str:
    return _run(lambda: get_client().get("/api/v1/rentals"))


def get_rental(rental_id: str) -> str:
    return _run(lambda: get_client().get(f"/api/v1/rentals/{rental_id}"))


def checkout_rental(vehicle_id: str) -> str:
    return _run(
        lambda: get_client().post(
            "/api/v1/rentals/checkout",
            json_body={"vehicle_id": vehicle_id},
        )
    )


def return_rental(rental_id: str, station_id: str) -> str:
    return _run(
        lambda: get_client().post(
            f"/api/v1/rentals/{rental_id}/return",
            json_body={"station_id": station_id},
        )
    )


def record_rental_payment(rental_id: str) -> str:
    return _run(lambda: get_client().post(f"/api/v1/rentals/{rental_id}/record-payment"))


# --- Phase 2: writes + seed ---


def create_vehicle_type(name: str, current_rate: float) -> str:
    return _run(
        lambda: get_client().post(
            "/api/v1/vehicle-types",
            json_body={"name": name, "current_rate": current_rate},
        )
    )


def update_vehicle_type(
    vehicle_type_id: str,
    name: str | None = None,
    current_rate: float | None = None,
) -> str:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if current_rate is not None:
        body["current_rate"] = current_rate
    return _run(lambda: get_client().patch(f"/api/v1/vehicle-types/{vehicle_type_id}", body))


def delete_vehicle_type(vehicle_type_id: str) -> str:
    return _run(lambda: get_client().delete(f"/api/v1/vehicle-types/{vehicle_type_id}"))


def create_station(name: str, capacity: int, latitude: float, longitude: float) -> str:
    return _run(
        lambda: get_client().post(
            "/api/v1/stations",
            json_body={
                "name": name,
                "capacity": capacity,
                "latitude": latitude,
                "longitude": longitude,
            },
        )
    )


def update_station(
    station_id: str,
    name: str | None = None,
    capacity: int | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> str:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if capacity is not None:
        body["capacity"] = capacity
    if latitude is not None:
        body["latitude"] = latitude
    if longitude is not None:
        body["longitude"] = longitude
    return _run(lambda: get_client().patch(f"/api/v1/stations/{station_id}", body))


def delete_station(station_id: str) -> str:
    return _run(lambda: get_client().delete(f"/api/v1/stations/{station_id}"))


def create_vehicle(vehicle_type_id: str, station_id: str) -> str:
    return _run(
        lambda: get_client().post(
            "/api/v1/vehicles",
            json_body={"vehicle_type_id": vehicle_type_id, "station_id": station_id},
        )
    )


def update_vehicle(
    vehicle_id: str,
    vehicle_type_id: str | None = None,
    station_id: str | None = None,
) -> str:
    body: dict[str, Any] = {}
    if vehicle_type_id is not None:
        body["vehicle_type_id"] = vehicle_type_id
    if station_id is not None:
        body["station_id"] = station_id
    return _run(lambda: get_client().patch(f"/api/v1/vehicles/{vehicle_id}", body))


def delete_vehicle(vehicle_id: str) -> str:
    return _run(lambda: get_client().delete(f"/api/v1/vehicles/{vehicle_id}"))


def seed_network() -> str:
    """Populate an empty database with demo Tandil network. Fails with 409 if data already exists."""
    return _run(lambda: get_client().post("/api/v1/seed"))
