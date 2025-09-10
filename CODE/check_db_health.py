#!/usr/bin/env python3
"""
Script para verificar la salud de la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.database import get_db, init_db
from src.models.message import Message
from src.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

def check_database_health():
    """Verificar la salud de la base de datos"""
    print("🔍 Verificando salud de la base de datos...")
    
    try:
        # Inicializar base de datos
        init_db()
        print("✅ Base de datos inicializada correctamente")
        
        # Obtener sesión
        db_gen = get_db()
        db: Session = next(db_gen)
        
        try:
            # Verificar conexión
            db.execute(text("SELECT 1"))
            print("✅ Conexión a base de datos exitosa")
            
            # Verificar tabla de usuarios
            user_count = db.query(User).count()
            print(f"✅ Tabla usuarios: {user_count} registros")
            
            # Verificar tabla de mensajes
            message_count = db.query(Message).count()
            print(f"✅ Tabla mensajes: {message_count} registros")
            
            # Verificar mensajes no leídos
            unread_count = db.query(Message).filter(Message.is_read == False).count()
            print(f"✅ Mensajes no leídos: {unread_count}")
            
            # Verificar mensajes pendientes
            pending_count = db.query(Message).filter(
                Message.is_read == True,
                Message.admin_response.is_(None)
            ).count()
            print(f"✅ Mensajes pendientes: {pending_count}")
            
            # Verificar mensajes cerrados
            closed_count = db.query(Message).filter(Message.admin_response.isnot(None)).count()
            print(f"✅ Mensajes cerrados: {closed_count}")
            
            print("\n🎉 Base de datos saludable")
            
        except Exception as e:
            print(f"❌ Error en consultas: {e}")
            return False
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = check_database_health()
    sys.exit(0 if success else 1)
