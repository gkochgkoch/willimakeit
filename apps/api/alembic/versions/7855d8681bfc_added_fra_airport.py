"""Added FRA airport

Revision ID: 7855d8681bfc
Revises: 2e553063d683
Create Date: 2026-08-12 15:24:51.791121

"""

from typing import Sequence, Union
from uuid import UUID

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7855d8681bfc"
down_revision: Union[str, Sequence[str], None] = "2e553063d683"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

airports = sa.table(
    "airports",
    sa.Column("id", sa.Uuid()),
    sa.Column("airport_code", sa.String()),
    sa.Column("name", sa.String()),
    sa.Column("latitude", sa.Float()),
    sa.Column("longitude", sa.Float()),
)


def upgrade() -> None:
    op.execute(
        sa.insert(airports).values(
            id=UUID("10000000-0000-0000-0000-000000000003"),
            airport_code="FRA",
            name="Frankfurt Airport",
            latitude=50.0379,
            longitude=8.5622,
        )
    )


def downgrade() -> None:
    op.execute(sa.delete(airports).where(airports.c.airport_code == "FRA"))
    pass
