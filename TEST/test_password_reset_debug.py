#!/usr/bin/env python3
"""
Script de depuración para el problema de password reset
"""

import sys
import os
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

async def test_password_reset_debug():
    """Probar la funcionalidad de password reset paso a paso"""
    print("🔍 DEPURACIÓN DE PASSWORD RESET")
    print("=" * 50)
    
    try:
        from src.database.database import get_db
        from src.models.user import User
        from src.models.password_reset import PasswordResetToken
        from src.services.user_service import UserService
        from src.utils.datetime_utils import get_colombia_now
        
        # Obtener sesión de base de datos
        db = next(get_db())
        user_service = UserService(db)
        
        # Buscar usuario jveyes@gmail.com
        print("1. Buscando usuario jveyes@gmail.com...")
        user = user_service.get_user_by_email("jveyes@gmail.com")
        if not user:
            print("❌ Usuario no encontrado")
            return
        print(f"✅ Usuario encontrado: {user.username} ({user.email})")
        
        # Verificar tokens existentes
        print("\n2. Verificando tokens existentes...")
        existing_tokens = db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.is_used == False
        ).all()
        print(f"✅ Tokens existentes: {len(existing_tokens)}")
        
        # Marcar tokens como usados manualmente
        print("\n3. Marcando tokens como usados...")
        for token in existing_tokens:
            print(f"   - Token: {token.token[:8]}... (usado: {token.is_used})")
            token.is_used = True
            token.used_at = get_colombia_now()
        
        # Hacer commit
        print("\n4. Haciendo commit...")
        db.commit()
        print("✅ Commit exitoso")
        
        # Crear nuevo token
        print("\n5. Creando nuevo token...")
        new_token = PasswordResetToken.create_token(user.id)
        print(f"✅ Nuevo token creado: {new_token.token[:8]}...")
        
        # Agregar a la base de datos
        print("\n6. Agregando token a la base de datos...")
        db.add(new_token)
        db.commit()
        print("✅ Token agregado exitosamente")
        
        print("\n🎉 PRUEBA EXITOSA - No hay problemas con updated_at")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_password_reset_debug())
