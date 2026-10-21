"""add unpublished to vehicle status

Revision ID: b7e4a1c2d9f0
Revises: a3c1d9e7b2f4
Create Date: 2026-10-21 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b7e4a1c2d9f0'
down_revision: Union[str, Sequence[str], None] = 'a3c1d9e7b2f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ALTER TYPE ... ADD VALUE no puede usarse en la misma transaccion en
    # versiones viejas de PostgreSQL, por eso va en un bloque autocommit.
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE status ADD VALUE IF NOT EXISTS 'unpublished'")


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL no permite quitar valores de un enum. Se reasignan los
    # vehiculos afectados y el valor queda en el tipo (inofensivo).
    op.execute("UPDATE vehicles SET status = 'available' WHERE status = 'unpublished'")
