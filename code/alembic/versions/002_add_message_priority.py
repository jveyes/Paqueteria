"""Add priority field to messages table

Revision ID: 002_add_message_priority
Revises: 001_initial_migration
Create Date: 2025-01-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_message_priority'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # Add priority column to messages table
    op.add_column('messages', sa.Column('priority', sa.Enum('low', 'normal', 'high', 'urgent', name='messagepriority'), nullable=True))
    
    # Set default priority to 'normal' for existing messages
    op.execute("UPDATE messages SET priority = 'normal' WHERE priority IS NULL")
    
    # Make the column not nullable after setting defaults
    op.alter_column('messages', 'priority', nullable=False)


def downgrade():
    # Remove priority column
    op.drop_column('messages', 'priority')