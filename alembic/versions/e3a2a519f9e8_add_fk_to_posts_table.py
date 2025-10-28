"""add fk to posts table

Revision ID: e3a2a519f9e8
Revises: b36684a2d348
Create Date: 2025-10-28 21:49:54.153770

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3a2a519f9e8"
down_revision: Union[str, Sequence[str], None] = "b36684a2d348"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
