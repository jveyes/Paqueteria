"""rename phone_number to customer_phone

Revision ID: 003_rename_phone_number_to_customer_phone
Revises: fe004bd9af7f
Create Date: 2025-01-09 14:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_rename_phone'
down_revision = 'fe004bd9af7f'
branch_labels = None
depends_on = None


def upgrade():
    # Renombrar la columna phone_number a customer_phone en package_announcements
    op.alter_column('package_announcements', 'phone_number', new_column_name='customer_phone')


def downgrade():
    # Revertir el cambio
    op.alter_column('package_announcements', 'customer_phone', new_column_name='phone_number')
