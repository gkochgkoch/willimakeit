"""Seed airports

Revision ID: 2e553063d683
Revises: 1a7b437bdfbf
Create Date: 2026-08-10 12:34:53.506545

"""

from typing import Sequence, Union
from uuid import UUID

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2e553063d683"
down_revision: Union[str, Sequence[str], None] = "1a7b437bdfbf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

airports = sa.table(
    "airports",
    sa.Column("id", sa.Uuid(), nullable=False),
    sa.Column("airport_code", sa.String(length=3), nullable=False),
    sa.Column("name", sa.String(length=50), nullable=False),
    sa.Column("latitude", sa.Float(), nullable=False),
    sa.Column("longitude", sa.Float(), nullable=False),
)


def upgrade() -> None:
    op.bulk_insert(
        airports,
        [
            {
                "id": UUID("10000000-0000-0000-0000-000000000001"),
                "airport_code": "LHR",
                "name": "London Heathrow",
                "latitude": 51.4704,
                "longitude": -0.4586,
            },
            {
                "id": UUID("10000000-0000-0000-0000-000000000002"),
                "airport_code": "CDG",
                "name": "Charles de Gaulle Airport",
                "latitude": 49.0089700583481,
                "longitude": 2.551040303145449,
            },
        ],
    )


def downgrade() -> None:
    op.execute(sa.delete(airports).where(airports.c.airport_code.in_(["LHR", "CDG"])))
