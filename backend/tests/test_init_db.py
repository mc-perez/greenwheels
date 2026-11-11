"""Scenario: No create_all on PostgreSQL startup."""

from unittest.mock import MagicMock, patch

from app import db


def test_init_db_does_not_create_all_on_postgresql():
    with patch.object(db.SQLModel.metadata, "create_all") as create_all:
        with patch.object(db, "settings") as settings:
            settings.database_url = "postgresql+psycopg://greenwheels:greenwheels@db:5432/greenwheels"
            db.init_db()
            create_all.assert_not_called()


def test_init_db_uses_create_all_on_sqlite():
    mock_engine = MagicMock()
    with patch.object(db.SQLModel.metadata, "create_all") as create_all:
        with patch.object(db, "settings") as settings:
            with patch.object(db, "engine", mock_engine):
                settings.database_url = "sqlite://"
                db.init_db()
                create_all.assert_called_once_with(mock_engine)
