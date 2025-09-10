#!/usr/bin/env python3
"""
Script de prueba para el servicio de notificaciones
"""

import sys
import os
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

async def test_notification_service():
    """Probar el servicio de notificaciones"""
    print("🔍 PRUEBA DEL SERVICIO DE NOTIFICACIONES")
    print("=" * 50)
    
    try:
        from src.database.database import get_db
        from src.models.user import User
        from src.services.notification_service import NotificationService
        
        # Obtener sesión de base de datos
        db = next(get_db())
        notification_service = NotificationService(db)
        
        # Buscar usuario jveyes@gmail.com
        print("1. Buscando usuario jveyes@gmail.com...")
        user = db.query(User).filter(User.email == "jveyes@gmail.com").first()
        if not user:
            print("❌ Usuario no encontrado")
            return
        print(f"✅ Usuario encontrado: {user.username} ({user.email})")
        
        # Probar envío de email
        print("\n2. Probando envío de email...")
        subject = "Prueba de Notificación - PAQUETES EL CLUB"
        message = """
        <h2>Prueba de Notificación</h2>
        <p>Este es un email de prueba para verificar que el servicio de notificaciones funciona correctamente.</p>
        <p><strong>Fecha:</strong> {}</p>
        <p><strong>Usuario:</strong> {}</p>
        """.format("2025-09-09 13:37:00", user.username)
        
        success = await notification_service._send_email(
            to_email=user.email,
            subject=subject,
            message=message
        )
        
        if success:
            print("✅ Email enviado exitosamente")
        else:
            print("❌ Error al enviar email")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_notification_service())
