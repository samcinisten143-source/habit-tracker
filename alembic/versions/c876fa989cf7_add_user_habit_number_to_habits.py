"""add user_habit_number to habits

Revision ID: c876fa989cf7
Revises: 8d419d7a9b8b
Create Date: 2025-11-17 12:29:28.695016
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c876fa989cf7'
down_revision: Union[str, Sequence[str], None] = '8d419d7a9b8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1) Add column as nullable first
    op.add_column(
        'habits',
        sa.Column('user_habit_number', sa.Integer(), nullable=True)
    )

    # 2) Populate existing rows with per-user numbering
    op.execute("""
        WITH ranked AS (
            SELECT id,
                   ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id) AS rn
            FROM habits
        )
        UPDATE habits h
        SET user_habit_number = ranked.rn
        FROM ranked
        WHERE h.id = ranked.id;
    """)

    # 3) Now enforce NOT NULL
    op.alter_column('habits', 'user_habit_number', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('habits', 'user_habit_number')
