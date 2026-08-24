"""add condition to vehicles

Revision ID: 0333d2d77020
Revises: 469572dc2184
Create Date: 2026-08-23 22:03:44.890722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0333d2d77020'
down_revision: Union[str, Sequence[str], None] = '469572dc2184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    condition_enum = sa.Enum('new', 'used', name='condition')
    condition_enum.create(op.get_bind())
    op.add_column('vehicles', sa.Column('condition', condition_enum, nullable=True))


def downgrade() -> None:
    op.drop_column('vehicles', 'condition')
    sa.Enum(name='condition').drop(op.get_bind())
