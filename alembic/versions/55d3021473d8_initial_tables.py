"""initial tables

Revision ID: 55d3021473d8
Revises: 
Create Date: 2025-06-30 20:08:34.189267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55d3021473d8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Since this is the initial migration, create any foundational tables here if needed
    # For example, if you want to create users table here instead of separate migration, do it here
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # Drop any tables created in upgrade if needed
    pass
