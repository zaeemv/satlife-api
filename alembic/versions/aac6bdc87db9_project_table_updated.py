"""Project table updated

Revision ID: aac6bdc87db9
Revises: ffb2f55ee11c
Create Date: 2026-03-04 22:35:20.551647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'aac6bdc87db9'
down_revision: Union[str, Sequence[str], None] = 'ffb2f55ee11c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'user' in inspector.get_table_names():
        column_names = {column['name'] for column in inspector.get_columns('user')}
        if 'password' not in column_names:
            op.add_column('user', sa.Column('password', sa.String(), nullable=True))
        if 'hashed_password' in column_names:
            op.drop_column('user', 'hashed_password')


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'user' in inspector.get_table_names():
        column_names = {column['name'] for column in inspector.get_columns('user')}
        if 'hashed_password' not in column_names:
            op.add_column('user', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True))
        if 'password' in column_names:
            op.drop_column('user', 'password')
