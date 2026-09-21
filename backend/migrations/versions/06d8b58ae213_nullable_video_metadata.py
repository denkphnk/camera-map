"""nullable video_metadata

Revision ID: 06d8b58ae213
Revises: 10c5ab9b9461
Create Date: 2026-09-21 10:42:59.260743

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "06d8b58ae213"
down_revision: Union[str, Sequence[str], None] = "10c5ab9b9461"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
