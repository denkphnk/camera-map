"""nullable video_preview

Revision ID: 10c5ab9b9461
Revises: 6ce5312e9a78
Create Date: 2026-09-21 10:16:42.379884

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "10c5ab9b9461"
down_revision: Union[str, Sequence[str], None] = "6ce5312e9a78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
