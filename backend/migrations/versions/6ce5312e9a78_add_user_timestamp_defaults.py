"""add user timestamp defaults

Revision ID: 6ce5312e9a78
Revises: 601a04bc3cad
Create Date: 2026-09-11 11:24:31.962429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ce5312e9a78'
down_revision: Union[str, Sequence[str], None] = '601a04bc3cad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "created_at",
        server_default=sa.text("now()"),
    )

    op.alter_column(
        "users",
        "updated_at",
        server_default=sa.text("now()"),
    )


def downgrade():
    op.alter_column(
        "users",
        "created_at",
        server_default=None,
    )

    op.alter_column(
        "users",
        "updated_at",
        server_default=None,
    )
