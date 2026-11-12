"""fleet vehicle table

Revision ID: 0003_fleet_vehicle
Revises: 0002_stations_and_unique_names
Create Date: 2026-11-11

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003_fleet_vehicle"
down_revision: Union[str, Sequence[str], None] = "0002_stations_and_unique_names"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vehicle",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("vehicle_type_id", sa.Uuid(), nullable=False),
        sa.Column("parked_station_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["vehicle_type_id"], ["vehicle_type.id"]),
        sa.ForeignKeyConstraint(["parked_station_id"], ["station.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_vehicle_vehicle_type_id", "vehicle", ["vehicle_type_id"])
    op.create_index("ix_vehicle_parked_station_id", "vehicle", ["parked_station_id"])


def downgrade() -> None:
    op.drop_index("ix_vehicle_parked_station_id", table_name="vehicle")
    op.drop_index("ix_vehicle_vehicle_type_id", table_name="vehicle")
    op.drop_table("vehicle")
