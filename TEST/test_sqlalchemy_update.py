#!/usr/bin/env python3
"""
Script para probar el problema específico de SQLAlchemy con updated_at
"""

import sys
import os
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

def test_sqlalchemy_update():
    """Probar el problema específico de SQLAlchemy"""
    print("🔍 PRUEBA ESPECÍFICA DE SQLALCHEMY")
    print("=" * 50)
    
    try:
        from src.database.database import get_db
        from src.models.password_reset import PasswordResetToken
        from src.utils.datetime_utils import get_colombia_now
        
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Buscar un token existente
        print("1. Buscando token existente...")
        token = db.query(PasswordResetToken).filter(
            PasswordResetToken.is_used == False
        ).first()
        
        if not token:
            print("❌ No hay tokens disponibles")
            return
        
        print(f"✅ Token encontrado: {token.token[:8]}...")
        print(f"   - is_used: {token.is_used}")
        print(f"   - used_at: {token.used_at}")
        
        # Intentar actualizar el token
        print("\n2. Actualizando token...")
        token.is_used = True
        token.used_at = get_colombia_now()
        
        print("3. Haciendo commit...")
        db.commit()
        print("✅ Commit exitoso")
        
        print("\n🎉 ACTUALIZACIÓN EXITOSA")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    test_sqlalchemy_update()
