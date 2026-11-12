"""rental table

Revision ID: 0004_rental
Revises: 0003_fleet_vehicle
Create Date: 2026-11-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004_rental"
down_revision: Union[str, Sequence[str], None] = "0003_fleet_vehicle"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rental",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("vehicle_id", sa.Uuid(), nullable=False),
        sa.Column("checkout_station_id", sa.Uuid(), nullable=False),
        sa.Column("return_station_id", sa.Uuid(), nullable=True),
        sa.Column("rate_at_checkout", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("amount_owed", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicle.id"]),
        sa.ForeignKeyConstraint(["checkout_station_id"], ["station.id"]),
        sa.ForeignKeyConstraint(["return_station_id"], ["station.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rental_vehicle_id", "rental", ["vehicle_id"])
    op.create_index(
        "uq_rental_one_open_per_vehicle",
        "rental",
        ["vehicle_id"],
        unique=True,
        postgresql_where=sa.text("ended_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_rental_one_open_per_vehicle", table_name="rental")
    op.drop_index("ix_rental_vehicle_id", table_name="rental")
    op.drop_table("rental")
