#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad SMTP desde la aplicación
"""

import asyncio
import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

async def test_notification_service():
    """Probar el servicio de notificaciones de la aplicación"""
    print("🔍 Probando servicio de notificaciones de la aplicación...")
    
    try:
        # Importar dependencias de la aplicación
        from src.services.notification_service import NotificationService
        from src.database.database import get_db
        from src.models.user import User, UserRole
        
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Crear servicio de notificaciones
        notification_service = NotificationService(db)
        
        # Crear un usuario de prueba
        test_user = User(
            id="00000000-0000-0000-0000-000000000001",
            username="test_user",
            email="jveyes@gmail.com",
            full_name="Usuario de Prueba",
            role=UserRole.USER,
            is_active=True
        )
        
        # Crear token de reset de prueba
        test_token = "test_token_12345"
        
        print("📧 Enviando email de restablecimiento de contraseña...")
        
        # Probar envío de email de reset de contraseña
        email_sent = await notification_service.send_password_reset_email(test_user, test_token)
        
        if email_sent:
            print("✅ Email de restablecimiento enviado exitosamente")
            return True
        else:
            print("❌ Error enviando email de restablecimiento")
            return False
            
    except Exception as e:
        print(f"❌ Error en el servicio de notificaciones: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

async def test_direct_email():
    """Probar envío directo de email usando el servicio"""
    print("\n🔍 Probando envío directo de email...")
    
    try:
        from src.services.notification_service import NotificationService
        from src.database.database import get_db
        
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Crear servicio de notificaciones
        notification_service = NotificationService(db)
        
        # Contenido del email de prueba
        subject = "🧪 Prueba Directa - PAQUETES EL CLUB v3.5"
        message = f"""
        <h2>✅ Prueba de Email Directo</h2>
        <p>Este es un email de prueba enviado directamente desde el servicio de notificaciones de la aplicación.</p>
        
        <h3>📋 Información de la Prueba:</h3>
        <ul>
            <li><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            <li><strong>Método:</strong> Servicio de Notificaciones</li>
            <li><strong>Estado:</strong> FUNCIONANDO</li>
        </ul>
        
        <p>Si recibes este email, significa que el servicio de notificaciones está operativo.</p>
        """
        
        print("📧 Enviando email directo...")
        
        # Enviar email directo
        notification = await notification_service.send_email_notification(
            to_email="jveyes@gmail.com",
            subject=subject,
            message=message
        )
        
        if notification and notification.status.value == "sent":
            print("✅ Email directo enviado exitosamente")
            return True
        else:
            print("❌ Error enviando email directo")
            return False
            
    except Exception as e:
        print(f"❌ Error en envío directo: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

async def main():
    """Función principal"""
    print("=" * 70)
    print("🧪 PRUEBA DE SERVICIO DE NOTIFICACIONES - PAQUETES EL CLUB v3.5")
    print("=" * 70)
    
    # Probar servicio de notificaciones
    service_ok = await test_notification_service()
    
    # Probar envío directo
    direct_ok = await test_direct_email()
    
    print("\n" + "=" * 70)
    if service_ok and direct_ok:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("=" * 70)
        print("✅ El servicio de notificaciones está funcionando correctamente")
        print("✅ Los emails se están enviando desde la aplicación")
        print("📧 Revisa jveyes@gmail.com para confirmar la recepción")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("=" * 70)
        if not service_ok:
            print("❌ Error en el servicio de notificaciones")
        if not direct_ok:
            print("❌ Error en el envío directo")

if __name__ == "__main__":
    asyncio.run(main())
