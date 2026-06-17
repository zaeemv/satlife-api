"""Update inventory table to support multiple entity types

Revision ID: e8f4a9c1d2e3
Revises: d671fa45ec45
Create Date: 2026-06-17 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8f4a9c1d2e3'
down_revision: Union[str, Sequence[str], None] = 'd671fa45ec45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to support inventory for all entity types."""
    # Drop the foreign key constraint to component
    op.drop_constraint('inventory_component_id_fkey', 'inventory', type_='foreignkey')
    
    # Drop the component_id column
    op.drop_column('inventory', 'component_id')
    
    # Add new columns for multi-entity-type inventory
    op.add_column('inventory', sa.Column('name', sa.String(), nullable=False, server_default='Unknown'))
    op.add_column('inventory', sa.Column('inventory_type', sa.String(), nullable=False, server_default='component'))
    op.add_column('inventory', sa.Column('serial_number', sa.String(), nullable=True))
    op.add_column('inventory', sa.Column('description', sa.String(), nullable=True))
    op.add_column('inventory', sa.Column('oem_name', sa.String(), nullable=True))
    op.add_column('inventory', sa.Column('manufacturer_part_number', sa.String(), nullable=True))
    op.add_column('inventory', sa.Column('entity_id', sa.Integer(), nullable=True))
    
    # Add index on entity_id for better query performance
    op.create_index('ix_inventory_entity_id', 'inventory', ['entity_id'])
    
    # Remove server defaults after they're applied
    op.alter_column('inventory', 'name', server_default=None)
    op.alter_column('inventory', 'inventory_type', server_default=None)


def downgrade() -> None:
    """Downgrade schema back to component-only inventory."""
    # Drop the entity_id column and related index
    op.drop_index('ix_inventory_entity_id', 'inventory')
    op.drop_column('inventory', 'entity_id')
    
    # Drop the new columns
    op.drop_column('inventory', 'manufacturer_part_number')
    op.drop_column('inventory', 'oem_name')
    op.drop_column('inventory', 'description')
    op.drop_column('inventory', 'serial_number')
    op.drop_column('inventory', 'inventory_type')
    op.drop_column('inventory', 'name')
    
    # Re-add component_id column with foreign key
    op.add_column('inventory', sa.Column('component_id', sa.Integer(), nullable=False))
    op.create_foreign_key('inventory_component_id_fkey', 'inventory', 'component', ['component_id'], ['id'])
