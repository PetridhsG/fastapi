"""add columns to posts table:

Revision ID: 16a230a5bdc9
Revises: e3a2a519f9e8
Create Date: 2025-10-28 21:55:26.058154

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "16a230a5bdc9"
down_revision: Union[str, Sequence[str], None] = "e3a2a519f9e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
