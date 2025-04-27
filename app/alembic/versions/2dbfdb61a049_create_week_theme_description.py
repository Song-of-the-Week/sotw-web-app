"""create week theme description

Revision ID: 2dbfdb61a049
Revises: 3cdc47c4eb91
Create Date: 2025-04-27 10:37:20.788612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dbfdb61a049'
down_revision: Union[str, None] = '3cdc47c4eb91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "week",
        sa.Column("theme_description", sa.String(), nullable=True),
    )


def downgrade() -> None:
        op.drop_column("week", "theme_description")

