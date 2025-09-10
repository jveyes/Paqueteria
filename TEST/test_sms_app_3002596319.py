#!/usr/bin/env python3
"""
Script para probar SMS desde la aplicación con el número 3002596319
"""

import sys
import os
import asyncio
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

async def test_sms_from_app_3002596319():
    """Probar SMS desde la aplicación con el número 3002596319"""
    print("🔍 PRUEBA SMS DESDE APLICACIÓN CON 3002596319")
    print("=" * 50)
    
    try:
        from src.database.database import get_db
        from src.services.notification_service import NotificationService
        from src.models.package import Package
        
        # Obtener sesión de base de datos
        db = next(get_db())
        notification_service = NotificationService(db)
        
        # Buscar un paquete existente o crear uno de prueba
        print("1. Buscando paquete existente...")
        package = db.query(Package).first()
        
        if not package:
            print("❌ No hay paquetes en la base de datos")
            return
        
        print(f"✅ Paquete encontrado: {package.tracking_number}")
        print(f"   - Cliente: {package.customer_name}")
        print(f"   - Teléfono original: {package.customer_phone}")
        
        # Actualizar temporalmente el teléfono para la prueba
        original_phone = package.customer_phone
        package.customer_phone = "3002596319"
        print(f"   - Teléfono de prueba: {package.customer_phone}")
        
        # Probar envío de SMS de anuncio
        print("\n2. Probando envío de SMS de anuncio...")
        try:
            result = await notification_service.send_package_announcement(package)
            print(f"✅ SMS de anuncio enviado")
            print(f"   - Estado: {result.status}")
            print(f"   - Mensaje: {result.message[:50]}...")
        except Exception as e:
            print(f"❌ Error en SMS de anuncio: {e}")
        
        # Probar envío de SMS de notificación de recepción
        print("\n3. Probando envío de SMS de notificación de recepción...")
        try:
            result = await notification_service.send_package_received(package)
            print(f"✅ SMS de notificación de recepción enviado")
            print(f"   - Estado: {result.status}")
            if result.error_message:
                print(f"   - Error: {result.error_message}")
        except Exception as e:
            print(f"❌ Error en SMS de notificación de recepción: {e}")
        
        # Probar envío de SMS de notificación de entrega
        print("\n4. Probando envío de SMS de notificación de entrega...")
        try:
            result = await notification_service.send_package_delivered(package)
            print(f"✅ SMS de notificación de entrega enviado")
            print(f"   - Estado: {result.status}")
            if result.error_message:
                print(f"   - Error: {result.error_message}")
        except Exception as e:
            print(f"❌ Error en SMS de notificación de entrega: {e}")
        
        # Restaurar el teléfono original
        package.customer_phone = original_phone
        print(f"\n✅ Teléfono restaurado a: {original_phone}")
        
        print("\n🎉 PRUEBAS DESDE APLICACIÓN COMPLETADAS")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    asyncio.run(test_sms_from_app_3002596319())
