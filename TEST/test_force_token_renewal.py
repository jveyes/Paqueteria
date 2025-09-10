#!/usr/bin/env python3
"""
Forzar la renovación del token para probar el manejo de expiración
"""

import asyncio
import aiohttp
import json

async def test_force_token_renewal():
    """Probar la renovación forzada del token"""
    print("🔄 PRUEBA DE RENOVACIÓN FORZADA DEL TOKEN")
    print("=" * 60)
    
    # Datos de prueba
    test_data = {
        "customer_name": "RENOVACIÓN TOKEN",
        "guide_number": "RENEW123",
        "tracking_code": "RT1"
    }
    
    print("📱 ENVIANDO SMS PARA PROBAR RENOVACIÓN DE TOKEN...")
    print(f"📞 Número: 3002596319")
    print(f"👤 Cliente: {test_data['customer_name']}")
    print(f"📦 Guía: {test_data['guide_number']}")
    print(f"🔑 Tracking: {test_data['tracking_code']}")
    print()
    
    # Enviar múltiples SMS para probar el manejo del token
    async with aiohttp.ClientSession() as session:
        for i in range(3):
            print(f"📤 ENVÍO {i+1}/3:")
            
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
                        print(f"   ✅ SMS {i+1} enviado exitosamente")
                        
                        # Mostrar respuesta de LIWA.co
                        liwa_response = result.get('liwa_response', {})
                        if liwa_response:
                            message_id = liwa_response.get('menssageId', 'N/A')
                            print(f"   📋 Message ID: {message_id}")
                        
                    else:
                        error_text = await response.text()
                        print(f"   ❌ Error en SMS {i+1}: {response.status} - {error_text}")
                        
            except Exception as e:
                print(f"   ❌ Excepción en SMS {i+1}: {e}")
            
            print()
            
            # Esperar entre envíos
            if i < 2:
                await asyncio.sleep(2)
    
    print("=" * 60)
    print("📊 VERIFICACIÓN DE LOGS:")
    print("=" * 60)
    print("Revisa los logs para confirmar:")
    print("✅ Autenticación exitosa con información de expiración")
    print("✅ Token renovado automáticamente si es necesario")
    print("✅ Múltiples SMS enviados correctamente")
    print()
    print("🔍 Comando para revisar logs:")
    print("   docker-compose logs app | grep -i 'token\|sms\|autenticación\|válido por' | tail -15")

if __name__ == "__main__":
    asyncio.run(test_force_token_renewal())
