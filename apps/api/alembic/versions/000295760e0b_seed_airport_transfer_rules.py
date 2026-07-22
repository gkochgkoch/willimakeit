"""seed airport transfer rules

Revision ID: 000295760e0b
Revises: fafb51b829f9
Create Date: 2026-07-22 12:28:58.239492

"""

from datetime import UTC, datetime
from typing import Sequence, Union
from uuid import UUID

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "000295760e0b"
down_revision: Union[str, Sequence[str], None] = "fafb51b829f9"
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
                "id": UUID("10000000-0000-0000-0000-000000000001"),
                "airport_code": "LHR",
                "arrival_terminal": "2",
                "departure_terminal": "5",
                "terminal_transfer_minutes": 30,
                "security_minutes": 20,
                "immigration_minutes": 10,
                "baggage_recheck_minutes": 0,
                "self_transfer": False,
                "source_type": "seed",
                "source_url": "dummy",
                "confidence": "low",
                "last_reviewed_at": datetime(
                    2026,
                    7,
                    22,
                    tzinfo=UTC,
                ),
            },
            {
                "id": UUID("10000000-0000-0000-0000-000000000002"),
                "airport_code": "FRA",
                "arrival_terminal": "1",
                "departure_terminal": "2",
                "terminal_transfer_minutes": 25,
                "security_minutes": 15,
                "immigration_minutes": 10,
                "baggage_recheck_minutes": 0,
                "self_transfer": False,
                "source_type": "seed",
                "source_url": "dummy",
                "confidence": "low",
                "last_reviewed_at": datetime(
                    2026,
                    7,
                    22,
                    tzinfo=UTC,
                ),
            },
            {
                "id": UUID("10000000-0000-0000-0000-000000000003"),
                "airport_code": "CDG",
                "arrival_terminal": "2E",
                "departure_terminal": "2F",
                "terminal_transfer_minutes": 25,
                "security_minutes": 20,
                "immigration_minutes": 10,
                "baggage_recheck_minutes": 0,
                "self_transfer": False,
                "source_type": "seed",
                "source_url": "dummy",
                "confidence": "low",
                "last_reviewed_at": datetime(
                    2026,
                    7,
                    22,
                    tzinfo=UTC,
                ),
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM airport_transfer_rules
            WHERE id IN (
                '10000000-0000-0000-0000-000000000001',
                '10000000-0000-0000-0000-000000000002',
                '10000000-0000-0000-0000-000000000003'
            )
            """
        )
    )
