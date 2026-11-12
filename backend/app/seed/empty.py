from sqlmodel import Session, select

from app.models.rental import Rental
from app.models.station import Station
from app.models.vehicle import Vehicle
from app.models.vehicle_type import VehicleType


def _has_any_row(session: Session, model: type) -> bool:
    return session.exec(select(model).limit(1)).first() is not None


def database_is_empty(session: Session) -> bool:
    return not (
        _has_any_row(session, Station)
        or _has_any_row(session, Vehicle)
        or _has_any_row(session, VehicleType)
        or _has_any_row(session, Rental)
    )


def database_is_seedable(session: Session) -> bool:
    return database_is_empty(session)
