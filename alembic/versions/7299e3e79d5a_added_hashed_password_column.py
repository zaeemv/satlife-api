"""Added hashed_password column

Revision ID: 7299e3e79d5a
Revises: 
Create Date: 2026-03-03 00:50:16.217132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlmodel import SQLModel


# revision identifiers, used by Alembic.
revision: str = '7299e3e79d5a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'user' in inspector.get_table_names():
        column_names = {column['name'] for column in inspector.get_columns('user')}
        if 'hashed_password' not in column_names:
            op.add_column('user', sa.Column('hashed_password', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'user' in inspector.get_table_names():
        column_names = {column['name'] for column in inspector.get_columns('user')}
        if 'hashed_password' in column_names:
            op.drop_column('user', 'hashed_password')
