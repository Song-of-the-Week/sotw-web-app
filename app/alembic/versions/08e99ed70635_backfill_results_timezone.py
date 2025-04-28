"""backfill results_timezone

Revision ID: 08e99ed70635
Revises: 98d0fe8cd496
Create Date: 2025-04-15 17:40:45.933560

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "08e99ed70635"
down_revision: Union[str, None] = "98d0fe8cd496"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "UPDATE sotw SET results_timezone = 'America/New_York' WHERE results_timezone IS NULL"
    )


def downgrade() -> None:
    op.execute(
        "UPDATE sotw SET results_timezone = NULL WHERE results_timezone IS NOT NULL"
    )
