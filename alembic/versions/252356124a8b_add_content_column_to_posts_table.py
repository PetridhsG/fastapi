"""add content column to posts table

Revision ID: 252356124a8b
Revises: fd4d01243bbb
Create Date: 2025-10-28 21:36:40.877793

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "252356124a8b"
down_revision: Union[str, Sequence[str], None] = "fd4d01243bbb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts", "content")
