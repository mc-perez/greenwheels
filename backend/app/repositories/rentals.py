from uuid import UUID

from sqlmodel import Session, select

from app.models.rental import Rental


class RentalRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, rental: Rental) -> Rental:
        self._session.add(rental)
        self._session.flush()
        self._session.refresh(rental)
        return rental

    def save(self, rental: Rental) -> Rental:
        self._session.add(rental)
        self._session.flush()
        self._session.refresh(rental)
        return rental

    def list_all(self) -> list[Rental]:
        return list(self._session.exec(select(Rental)).all())

    def get(self, rental_id: UUID) -> Rental | None:
        return self._session.get(Rental, rental_id)

    def get_open_for_vehicle(self, vehicle_id: UUID) -> Rental | None:
        statement = select(Rental).where(
            Rental.vehicle_id == vehicle_id,
            Rental.ended_at == None,  # noqa: E711
        )
        return self._session.exec(statement).first()

    def has_open_rental_for_vehicle(self, vehicle_id: UUID) -> bool:
        return self.get_open_for_vehicle(vehicle_id) is not None
