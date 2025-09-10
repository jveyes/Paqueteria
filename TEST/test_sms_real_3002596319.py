#!/usr/bin/env python3
"""
Test real de SMS al número 3002596319
Verificar que realmente se envíen los mensajes
"""

import asyncio
import aiohttp
import json

async def test_real_sms():
    """Probar envío real de SMS"""
    print("📱 PROBANDO ENVÍO REAL DE SMS AL 3002596319")
    print("=" * 60)
    
    # Datos de prueba
    test_data = {
        "customer_name": "JUAN PEREZ PEREZ",
        "customer_phone": "3002596319",
        "guide_number": "SMS123",
        "tracking_code": "TEST"
    }
    
    print(f"📋 Datos de prueba:")
    print(f"   Cliente: {test_data['customer_name']}")
    print(f"   Teléfono: {test_data['customer_phone']}")
    print(f"   Guía: {test_data['guide_number']}")
    print(f"   Tracking: {test_data['tracking_code']}")
    print()
    
    # Probar creación de anuncio (que debería enviar SMS)
    print("1️⃣ CREANDO ANUNCIO (debería enviar SMS automáticamente)...")
    
    async with aiohttp.ClientSession() as session:
        try:
            # Crear anuncio
            async with session.post(
                "http://localhost/api/announcements/",
                json=test_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Anuncio creado exitosamente")
                    print(f"   ID: {result.get('id')}")
                    print(f"   Tracking Code: {result.get('tracking_code')}")
                    print(f"   Estado: {result.get('status')}")
                    print()
                    
                    # Esperar un momento para que se procese el SMS
                    print("⏳ Esperando 5 segundos para procesamiento de SMS...")
                    await asyncio.sleep(5)
                    
                    # Verificar si hay logs de SMS
                    print("2️⃣ VERIFICANDO LOGS DEL SISTEMA...")
                    print("   (Revisa tu teléfono 3002596319 para ver si llegó el SMS)")
                    print()
                    
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Error creando anuncio: {response.status}")
                    print(f"   Error: {error_text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en la prueba: {e}")
            return False

async def test_sms_direct():
    """Probar SMS directo desde el navegador"""
    print("3️⃣ PROBANDO SMS DIRECTO DESDE NAVEGADOR...")
    print("   (Simulando envío desde el frontend)")
    
    sms_data = {
        "customer_name": "MARIA GONZALEZ",
        "customer_phone": "3002596319",
        "guide_number": "DIRECT456",
        "tracking_code": "DIR1"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # Simular envío desde navegador (con User-Agent)
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with session.post(
                "http://localhost/api/announcements/send-sms-browser",
                json=sms_data,
                headers=headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ SMS enviado exitosamente desde navegador")
                    print(f"   Resultado: {result}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Error enviando SMS: {response.status}")
                    print(f"   Error: {error_text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en SMS directo: {e}")
            return False

async def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS REALES DE SMS")
    print("=" * 60)
    
    # Prueba 1: Crear anuncio
    result1 = await test_real_sms()
    
    # Prueba 2: SMS directo
    result2 = await test_sms_direct()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DE LAS PRUEBAS:")
    print(f"   Anuncio con SMS: {'✅ EXITOSO' if result1 else '❌ FALLÓ'}")
    print(f"   SMS directo: {'✅ EXITOSO' if result2 else '❌ FALLÓ'}")
    print()
    
    if result1 or result2:
        print("📱 ¡REVISA TU TELÉFONO 3002596319!")
        print("   Deberías haber recibido al menos un SMS")
    else:
        print("❌ No se enviaron SMS. Revisar configuración.")
    
    print("\n🔍 PRÓXIMOS PASOS:")
    print("   1. Revisar logs del contenedor: docker-compose logs app")
    print("   2. Verificar configuración LIWA.co")
    print("   3. Comprobar conectividad de red")

if __name__ == "__main__":
    asyncio.run(main())
