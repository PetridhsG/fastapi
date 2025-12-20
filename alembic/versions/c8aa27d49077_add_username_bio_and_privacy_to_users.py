"""add username bio and privacy to users

Revision ID: c8aa27d49077
Revises: 5f8864182ef9
Create Date: 2025-12-20 18:50:52.112921
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c8aa27d49077"
down_revision: Union[str, Sequence[str], None] = "5f8864182ef9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add new columns safely (username initially nullable)
    op.add_column("users", sa.Column("username", sa.String(), nullable=True))
    op.add_column("users", sa.Column("bio", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column(
            "is_private",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    # 2. Backfill usernames for existing users
    op.execute(
        """
        UPDATE users
        SET username = 'user_' || id
        WHERE username IS NULL
        """
    )

    # 3. Enforce NOT NULL + uniqueness on username
    op.alter_column("users", "username", nullable=False)

    op.create_unique_constraint(
        "uq_users_username",
        "users",
        ["username"],
    )

    op.create_index(
        "ix_users_username",
        "users",
        ["username"],
    )


def downgrade() -> None:
    op.drop_index("ix_users_username", table_name="users")
    op.drop_constraint("uq_users_username", "users", type_="unique")
    op.drop_column("users", "is_private")
    op.drop_column("users", "bio")
    op.drop_column("users", "username")
