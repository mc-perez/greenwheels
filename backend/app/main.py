from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.router import api_router
from app.db import init_db
from app.ports.fleet_usage import FleetUsagePort


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    app.state.fleet_usage_port = None
    yield


app = FastAPI(title="GreenWheels API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(api_router, prefix="/api/v1")


def set_fleet_usage_port_for_tests(port: FleetUsagePort | None) -> None:
    app.state.fleet_usage_port = port
