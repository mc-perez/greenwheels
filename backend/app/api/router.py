from fastapi import APIRouter

from app.api import stations, vehicle_types

api_router = APIRouter()
api_router.include_router(vehicle_types.router)
api_router.include_router(stations.router)
