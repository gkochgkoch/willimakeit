"""Add airport transfer rules foreign key

Revision ID: ddd5c5fbdfbb
Revises: 7855d8681bfc
Create Date: 2026-08-12 15:42:42.727314

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ddd5c5fbdfbb"
down_revision: Union[str, Sequence[str], None] = "7855d8681bfc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_airport_transfer_rules_airport_code",
        "airport_transfer_rules",
        "airports",
        ["airport_code"],
        ["airport_code"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_airport_transfer_rules_airport_code",
        "airport_transfer_rules",
        type_="foreignkey",
    )
