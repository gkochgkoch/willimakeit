"""add cdg 2b to 2e transfer rule

Revision ID: 202607310001
Revises: 000295760e0b
Create Date: 2026-07-31 00:00:00.000000

"""

from datetime import UTC, datetime
from typing import Sequence, Union
from uuid import UUID

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "202607310001"
down_revision: Union[str, Sequence[str], None] = "000295760e0b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


airport_transfer_rules = sa.table(
    "airport_transfer_rules",
    sa.column("id", sa.Uuid()),
    sa.column("airport_code", sa.String()),
    sa.column("arrival_terminal", sa.String()),
    sa.column("departure_terminal", sa.String()),
    sa.column("terminal_transfer_minutes", sa.Integer()),
    sa.column("security_minutes", sa.Integer()),
    sa.column("immigration_minutes", sa.Integer()),
    sa.column("baggage_recheck_minutes", sa.Integer()),
    sa.column("self_transfer", sa.Boolean()),
    sa.column("source_type", sa.String()),
    sa.column("source_url", sa.String()),
    sa.column("confidence", sa.String()),
    sa.column("last_reviewed_at", sa.DateTime(timezone=True)),
)


def upgrade() -> None:
    op.bulk_insert(
        airport_transfer_rules,
        [
            {
                "id": UUID("10000000-0000-0000-0000-000000000004"),
                "airport_code": "CDG",
                "arrival_terminal": "2B",
                "departure_terminal": "2E",
                "terminal_transfer_minutes": 30,
                "security_minutes": 20,
                "immigration_minutes": 10,
                "baggage_recheck_minutes": 0,
                "self_transfer": False,
                "source_type": "seed",
                "source_url": "dummy",
                "confidence": "low",
                "last_reviewed_at": datetime(2026, 7, 31, tzinfo=UTC),
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM airport_transfer_rules
            WHERE id = '10000000-0000-0000-0000-000000000004'
            """
        )
    )
