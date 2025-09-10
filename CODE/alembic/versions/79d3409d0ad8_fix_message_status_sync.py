"""fix_message_status_sync

Revision ID: 79d3409d0ad8
Revises: 003_rename_phone
Create Date: 2025-09-09 20:20:55.180495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79d3409d0ad8'
down_revision = '003_rename_phone'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Sincronizar estados de mensajes basado en is_read y admin_response
    connection = op.get_bind()
    
    # Actualizar mensajes no leídos a UNREAD
    connection.execute(
        sa.text("""
            UPDATE messages 
            SET status = 'UNREAD' 
            WHERE is_read = false
        """)
    )
    
    # Actualizar mensajes con respuesta a CLOSED
    connection.execute(
        sa.text("""
            UPDATE messages 
            SET status = 'CLOSED' 
            WHERE admin_response IS NOT NULL AND admin_response != ''
        """)
    )
    
    # Actualizar mensajes leídos sin respuesta a PENDING
    connection.execute(
        sa.text("""
            UPDATE messages 
            SET status = 'PENDING' 
            WHERE is_read = true 
            AND (admin_response IS NULL OR admin_response = '')
        """)
    )


def downgrade() -> None:
    # No hay downgrade necesario para esta corrección de datos
    pass
