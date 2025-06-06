"""create week theme

Revision ID: 3cdc47c4eb91
Revises: 08e99ed70635
Create Date: 2025-04-26 18:24:41.793413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cdc47c4eb91'
down_revision: Union[str, None] = '08e99ed70635'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "response",
        sa.Column("theme", sa.String(), nullable=True),
    )
    op.add_column(
        "response",
        sa.Column("theme_description", sa.String(), nullable=True),
    )
    op.add_column(
        "results",
        sa.Column("theme", sa.String(), nullable=True),
    )
    op.add_column(
        "results",
        sa.Column("theme_description", sa.String(), nullable=True),
    )

def downgrade() -> None:
    op.drop_column("response", "theme")
    op.drop_column("response", "theme_description")
    op.drop_column("results", "theme")
    op.drop_column("results", "theme_description")
