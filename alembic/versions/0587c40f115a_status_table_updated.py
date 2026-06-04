"""status Table updated

Revision ID: 0587c40f115a
Revises: da5b26cf48ad
Create Date: 2026-03-08 11:48:15.400343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '0587c40f115a'
down_revision: Union[str, Sequence[str], None] = 'da5b26cf48ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'user' in inspector.get_table_names():
        op.execute("UPDATE \"user\" SET password = 'temp_password' WHERE password IS NULL")
        op.alter_column('user', 'password',
                   existing_type=sa.VARCHAR(),
                   nullable=False)
    if 'status' in inspector.get_table_names():
        column_names = {column['name'] for column in inspector.get_columns('status')}
        if 'status_type' not in column_names:
            op.add_column('status', sa.Column('status_type', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'user' in inspector.get_table_names():
        op.alter_column('user', 'password',
                   existing_type=sa.VARCHAR(),
                   nullable=True)
    if 'status' in inspector.get_table_names():
        column_names = {column['name'] for column in inspector.get_columns('status')}
        if 'status_type' in column_names:
            op.drop_column('status', 'status_type')
