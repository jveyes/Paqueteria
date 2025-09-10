#!/usr/bin/env python3
"""
Prueba final del manejo de tokens de LIWA.co
"""

import asyncio
import aiohttp
import json

async def test_token_management():
    """Probar el manejo mejorado del token"""
    print("🔑 PRUEBA FINAL DEL MANEJO DE TOKENS")
    print("=" * 60)
    
    # Datos de prueba
    test_data = {
        "customer_name": "PRUEBA TOKEN",
        "guide_number": "TOKEN123",
        "tracking_code": "TK1"
    }
    
    print("📱 ENVIANDO SMS CON MANEJO MEJORADO DE TOKEN...")
    print(f"📞 Número: 3002596319")
    print(f"👤 Cliente: {test_data['customer_name']}")
    print(f"📦 Guía: {test_data['guide_number']}")
    print(f"🔑 Tracking: {test_data['tracking_code']}")
    print()
    
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with session.post(
                "http://localhost/api/announcements/send-sms-browser",
                json=test_data,
                headers=headers
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ SMS ENVIADO EXITOSAMENTE")
                    print(f"📱 Número procesado: {result.get('phone', 'N/A')}")
                    print(f"📝 Mensaje: {result.get('message', 'N/A')}")
                    print(f"🔑 Tracking: {result.get('tracking_code', 'N/A')}")
                    
                    # Mostrar respuesta de LIWA.co
                    liwa_response = result.get('liwa_response', {})
                    if liwa_response:
                        print(f"🌐 LIWA.co Response: {json.dumps(liwa_response, indent=2)}")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ ERROR: {response.status} - {error_text}")
                    
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")
    
    print("\n" + "=" * 60)
    print("📊 VERIFICACIÓN DE LOGS:")
    print("=" * 60)
    print("Revisa los logs para confirmar:")
    print("✅ Autenticación exitosa con información de expiración")
    print("✅ Token renovado automáticamente si es necesario")
    print("✅ SMS enviado correctamente")
    print()
    print("🔍 Comando para revisar logs:")
    print("   docker-compose logs app | grep -i 'token\|sms\|autenticación' | tail -10")

if __name__ == "__main__":
    asyncio.run(test_token_management())
