"""add km_internal to vehicles

Revision ID: a3c1d9e7b2f4
Revises: 91cd203a741c
Create Date: 2026-10-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c1d9e7b2f4'
down_revision: Union[str, Sequence[str], None] = '91cd203a741c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('vehicles', sa.Column('km_internal', sa.Integer(), nullable=True))
    # Los vehiculos existentes tenian un unico km: pasa a ser tambien el interno.
    op.execute("UPDATE vehicles SET km_internal = km WHERE km IS NOT NULL")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('vehicles', 'km_internal')
