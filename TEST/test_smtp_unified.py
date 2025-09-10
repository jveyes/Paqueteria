#!/usr/bin/env python3
"""
Test SMTP después de unificación de términos
Probar con jveyes@gmail.com
"""

import asyncio
import sys
import os
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code/src')

from services.notification_service import NotificationService
from models.user import User
from database.database import get_db
from sqlalchemy.orm import Session

async def test_smtp_after_unification():
    """Probar SMTP después de unificación de términos"""
    print("🧪 PROBANDO SMTP DESPUÉS DE UNIFICACIÓN DE TÉRMINOS")
    print("=" * 60)
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Crear servicio de notificaciones
        notification_service = NotificationService(db)
        
        # Buscar usuario jveyes
        user = db.query(User).filter(User.email == "jveyes@gmail.com").first()
        
        if not user:
            print("❌ Usuario jveyes@gmail.com no encontrado")
            return False
        
        print(f"✅ Usuario encontrado: {user.full_name} ({user.email})")
        
        # Probar envío de email de restablecimiento de contraseña
        print("\n📧 Probando envío de email de restablecimiento de contraseña...")
        
        # Crear token de prueba
        reset_token = "test-token-unified-12345"
        
        # Enviar email
        result = await notification_service.send_password_reset_email(user, reset_token)
        
        if result:
            print("✅ Email de restablecimiento enviado exitosamente")
            print(f"📧 Email enviado a: {user.email}")
            print(f"🔗 Token: {reset_token}")
            print(f"🌐 URL: http://localhost/auth/reset-password?token={reset_token}")
        else:
            print("❌ Error enviando email de restablecimiento")
            return False
        
        # Probar envío de email de notificación
        print("\n📧 Probando envío de email de notificación...")
        
        # Crear notificación de prueba
        from models.notification import Notification, NotificationType, NotificationStatus
        
        test_notification = Notification(
            user_id=user.id,
            title="Test después de unificación",
            message="Esta es una notificación de prueba después de la unificación de términos",
            notification_type=NotificationType.EMAIL,
            status=NotificationStatus.PENDING
        )
        
        db.add(test_notification)
        db.commit()
        
        # Enviar notificación
        result = await notification_service.send_notification(test_notification)
        
        if result:
            print("✅ Notificación por email enviada exitosamente")
        else:
            print("❌ Error enviando notificación por email")
            return False
        
        print("\n🎉 TODAS LAS PRUEBAS SMTP EXITOSAS")
        return True
        
    except Exception as e:
        print(f"❌ Error en pruebas SMTP: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    result = asyncio.run(test_smtp_after_unification())
    if result:
        print("\n✅ SMTP funcionando correctamente después de unificación")
    else:
        print("\n❌ SMTP tiene problemas después de unificación")
