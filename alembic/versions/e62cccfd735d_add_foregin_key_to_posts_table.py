"""add foregin-key to posts table

Revision ID: e62cccfd735d
Revises: c3b965891054
Create Date: 2025-01-18 18:36:16.846496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e62cccfd735d'
down_revision: Union[str, None] = 'c3b965891054'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users",
                          local_cols= ['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
