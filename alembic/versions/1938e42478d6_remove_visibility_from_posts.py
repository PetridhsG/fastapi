"""Remove visibility from posts

Revision ID: 1938e42478d6
Revises: c8aa27d49077
Create Date: 2025-12-25 16:52:49.506981

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1938e42478d6"
down_revision: Union[str, Sequence[str], None] = "c8aa27d49077"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column("posts", "visibility")


def downgrade():
    op.add_column(
        "posts",
        sa.Column(
            "visibility",
            sa.Enum("public", "friends_only", name="post_visibility"),
            nullable=False,
            server_default="public",
        ),
    )
