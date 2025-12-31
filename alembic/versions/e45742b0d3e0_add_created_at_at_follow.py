"""Add created_at at follow

Revision ID: e45742b0d3e0
Revises: 1938e42478d6
Create Date: 2025-12-31 18:26:32.331148

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e45742b0d3e0"
down_revision: Union[str, Sequence[str], None] = "1938e42478d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "follows",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("follows", "created_at")
