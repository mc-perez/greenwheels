"""stations table and unique names

Revision ID: 0002_stations_and_unique_names
Revises: 0001_initial_vehicle_type
Create Date: 2026-11-11

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_stations_and_unique_names"
down_revision: Union[str, Sequence[str], None] = "0001_initial_vehicle_type"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_vehicle_type_name",
        "vehicle_type",
        ["name"],
        unique=True,
    )
    op.create_table(
        "station",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_station_name"),
    )


def downgrade() -> None:
    op.drop_table("station")
    op.drop_index("ix_vehicle_type_name", table_name="vehicle_type")
