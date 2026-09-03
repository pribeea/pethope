"""adiciona coluna foto em animal"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b123456789ab"
down_revision: Union[str, Sequence[str], None] = "a223b618bcc7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "animal",
        sa.Column("foto", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("animal", "foto")