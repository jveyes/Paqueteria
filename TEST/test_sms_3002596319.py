#!/usr/bin/env python3
"""
Script de prueba SMS para el número 3002596319
"""

import sys
import os
import asyncio
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

async def test_sms_3002596319():
    """Probar SMS con el número específico 3002596319"""
    print("🔍 PRUEBA SMS CON NÚMERO 3002596319")
    print("=" * 50)
    
    try:
        from src.services.sms_service import SMSService
        
        # Crear instancia del servicio SMS
        print("1. Creando instancia del servicio SMS...")
        sms_service = SMSService()
        print(f"✅ Servicio SMS creado")
        
        # Probar formateo del número específico
        print("\n2. Probando formateo del número 3002596319...")
        test_phone = "3002596319"
        try:
            formatted = sms_service._format_phone_number(test_phone)
            print(f"✅ Número formateado correctamente")
            print(f"   - Original: {test_phone}")
            print(f"   - Formateado: {formatted}")
        except Exception as e:
            print(f"❌ Error en formateo: {e}")
            return
        
        # Probar autenticación
        print("\n3. Probando autenticación con LIWA.co...")
        auth_result = await sms_service._authenticate()
        if auth_result:
            print("✅ Autenticación exitosa")
            print(f"   - Token obtenido: {sms_service._auth_token[:20]}...")
        else:
            print("❌ Error en autenticación")
            return
        
        # Probar envío de SMS de prueba
        print("\n4. Probando envío de SMS de prueba...")
        test_message = "Prueba de SMS desde PAQUETES EL CLUB - Sistema funcionando correctamente. Número de prueba: 3002596319"
        
        sms_result = await sms_service.send_notification_sms(
            phone=test_phone,
            message=test_message
        )
        
        if sms_result["success"]:
            print("✅ SMS enviado exitosamente")
            print(f"   - Teléfono: {sms_result['phone']}")
            print(f"   - Mensaje: {sms_result['message'][:50]}...")
            if 'liwa_response' in sms_result:
                print(f"   - ID LIWA: {sms_result['liwa_response'].get('id', 'N/A')}")
        else:
            print("❌ Error al enviar SMS")
            print(f"   - Error: {sms_result['error']}")
        
        # Probar envío de SMS de tracking
        print("\n5. Probando envío de SMS de tracking...")
        tracking_result = await sms_service.send_tracking_sms(
            phone=test_phone,
            customer_name="JUAN PEREZ PEREZ",
            tracking_code="TEST123456",
            guide_number="GUIA789"
        )
        
        if tracking_result["success"]:
            print("✅ SMS de tracking enviado exitosamente")
            print(f"   - Teléfono: {tracking_result['phone']}")
            print(f"   - Mensaje: {tracking_result['message'][:50]}...")
            print(f"   - Código de tracking: {tracking_result['tracking_code']}")
        else:
            print("❌ Error al enviar SMS de tracking")
            print(f"   - Error: {tracking_result['error']}")
        
        print("\n🎉 PRUEBAS COMPLETADAS")
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sms_3002596319())
