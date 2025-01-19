"""add content column to posts table

Revision ID: dd56a10fae08
Revises: 2ae17e9bda89
Create Date: 2025-01-17 18:17:57.016722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd56a10fae08'
down_revision: Union[str, None] = '2ae17e9bda89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
