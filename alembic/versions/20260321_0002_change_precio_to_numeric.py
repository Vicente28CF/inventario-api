"""change precio to numeric

Revision ID: 20260321_0002
Revises: 20260321_0001
Create Date: 2026-03-21 15:10:00

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260321_0002"
down_revision: str | Sequence[str] | None = "20260321_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("productos") as batch_op:
        batch_op.alter_column(
            "precio",
            existing_type=sa.Float(),
            type_=sa.Numeric(10, 2),
            existing_nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("productos") as batch_op:
        batch_op.alter_column(
            "precio",
            existing_type=sa.Numeric(10, 2),
            type_=sa.Float(),
            existing_nullable=False,
        )
