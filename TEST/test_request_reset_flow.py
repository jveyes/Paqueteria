#!/usr/bin/env python3
"""
Script que simula exactamente el flujo del endpoint request-reset
"""

import sys
import os
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

async def test_request_reset_flow():
    """Simular el flujo completo del endpoint request-reset"""
    print("🔍 SIMULACIÓN DEL FLUJO REQUEST-RESET")
    print("=" * 50)
    
    try:
        from src.database.database import get_db
        from src.models.user import User
        from src.services.user_service import UserService
        from src.services.notification_service import NotificationService
        
        # Obtener sesión de base de datos
        db = next(get_db())
        user_service = UserService(db)
        notification_service = NotificationService(db)
        
        email = "jveyes@gmail.com"
        
        print(f"1. Creando token de reset para {email}...")
        reset_token = user_service.create_password_reset_token(email)
        
        if not reset_token:
            print("❌ No se pudo crear el token")
            return
        
        print(f"✅ Token creado: {reset_token.token[:8]}...")
        
        print("\n2. Obteniendo usuario...")
        user = user_service.get_user_by_email(email)
        if not user:
            print("❌ Usuario no encontrado")
            return
        
        print(f"✅ Usuario encontrado: {user.username}")
        
        print("\n3. Enviando email de reset...")
        email_sent = await notification_service.send_password_reset_email(user, reset_token.token)
        
        if email_sent:
            print("✅ Email enviado exitosamente")
        else:
            print("❌ Error al enviar email")
        
        print("\n🎉 FLUJO COMPLETO EXITOSO")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_request_reset_flow())
