"""Add rag chunks

Revision ID: 97d3f72b94d5
Revises: ddd5c5fbdfbb
Create Date: 2026-08-14 12:48:56.431003

"""

from typing import Sequence, Union

import sqlalchemy as sa
from pgvector.sqlalchemy import VECTOR

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "97d3f72b94d5"
down_revision: Union[str, Sequence[str], None] = "ddd5c5fbdfbb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "airline_rule_chunks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("airline_code", sa.String(length=10), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("section", sa.String(length=100), nullable=True),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("embedding", VECTOR(1024), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("airline_rule_chunks")
