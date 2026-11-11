from uuid import UUID

from sqlmodel import Session, select

from app.models.station import Station


class StationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, station: Station) -> Station:
        self._session.add(station)
        self._session.flush()
        self._session.refresh(station)
        return station

    def list_all(self) -> list[Station]:
        return list(self._session.exec(select(Station)).all())

    def get(self, station_id: UUID) -> Station | None:
        return self._session.get(Station, station_id)

    def get_by_name(self, name: str) -> Station | None:
        statement = select(Station).where(Station.name == name)
        return self._session.exec(statement).first()

    def save(self, station: Station) -> Station:
        self._session.add(station)
        self._session.flush()
        self._session.refresh(station)
        return station

    def delete(self, station: Station) -> None:
        self._session.delete(station)
        self._session.flush()
