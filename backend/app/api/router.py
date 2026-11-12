from fastapi import APIRouter

from app.api import rentals, seed, stations, vehicle_types, vehicles

api_router = APIRouter()
api_router.include_router(vehicle_types.router)
api_router.include_router(stations.router)
api_router.include_router(vehicles.router)
api_router.include_router(rentals.router)
api_router.include_router(seed.router)
