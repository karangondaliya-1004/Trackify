"""add deleted_at to organizations and projects

Revision ID: a05c715b7d3a
Revises: 
Create Date: 2026-03-09 21:38:28.203951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a05c715b7d3a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "organizations",
        sa.Column("deleted_at", sa.DateTime(), nullable=True)
    )

    op.add_column(
        "projects",
        sa.Column("deleted_at", sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_column("organizations", "deleted_at")
    op.drop_column("projects", "deleted_at")