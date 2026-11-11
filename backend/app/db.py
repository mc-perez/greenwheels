from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.config import settings


def _create_engine(database_url: str):
    if database_url.startswith("sqlite"):
        return create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    return create_engine(database_url, echo=False)


engine = _create_engine(settings.database_url)


def init_db() -> None:
    from app import models  # noqa: F401 — register SQLModel tables before create_all

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
