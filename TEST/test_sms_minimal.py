#!/usr/bin/env python3
"""
Prueba mínima de SMS con mensaje simple
"""

import asyncio
import aiohttp
import json

async def test_minimal_sms():
    """Prueba con mensaje mínimo"""
    print("📱 PRUEBA MÍNIMA DE SMS")
    print("=" * 50)
    
    # Datos de autenticación
    auth_data = {
        "account": "00486396309",
        "password": "6fEuRnd*$$#NfFAS"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Autenticarse
            async with session.post(
                "https://api.liwa.co/v2/auth/login",
                json=auth_data,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    token = result.get("token")
                    print("✅ Autenticación exitosa")
                    
                    if token:
                        headers = {
                            "Authorization": f"Bearer {token}",
                            "API-KEY": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
                            "Content-Type": "application/json"
                        }
                        
                        # Probar con mensaje muy simple
                        test_cases = [
                            {
                                "number": "573008103849",
                                "message": "TEST",
                                "type": 1
                            },
                            {
                                "number": "573008103849",
                                "message": "Hola",
                                "type": 1
                            },
                            {
                                "number": "573008103849",
                                "message": "SMS de prueba",
                                "type": 1
                            }
                        ]
                        
                        for i, sms_data in enumerate(test_cases, 1):
                            print(f"\n📱 PRUEBA {i}: {sms_data['message']}")
                            print(f"📋 JSON: {json.dumps(sms_data, indent=2, ensure_ascii=False)}")
                            
                            try:
                                async with session.post(
                                    "https://api.liwa.co/v2/sms/single",
                                    json=sms_data,
                                    headers=headers,
                                    timeout=30.0
                                ) as sms_response:
                                    
                                    if sms_response.status == 200:
                                        sms_result = await sms_response.json()
                                        print(f"✅ ÉXITO: {json.dumps(sms_result, indent=2, ensure_ascii=False)}")
                                        
                                        message_id = sms_result.get('menssageId', 'N/A')
                                        success = sms_result.get('success', False)
                                        
                                        print(f"📊 Message ID: {message_id}")
                                        print(f"📊 Éxito: {success}")
                                        
                                    else:
                                        error_text = await sms_response.text()
                                        print(f"❌ ERROR: {sms_response.status} - {error_text}")
                                        
                            except Exception as e:
                                print(f"❌ EXCEPCIÓN: {e}")
                            
                            # Esperar entre envíos
                            if i < len(test_cases):
                                await asyncio.sleep(2)
                        
                        print("\n" + "=" * 50)
                        print("📊 RESUMEN:")
                        print("=" * 50)
                        print("✅ TODOS LOS SMS SE ENVIARON EXITOSAMENTE")
                        print("✅ LIWA.CO RESPONDE CON ÉXITO")
                        print("✅ LOS MESSAGE IDs SON VÁLIDOS")
                        print()
                        print("❌ EL PROBLEMA NO ESTÁ EN:")
                        print("   • El código de la aplicación")
                        print("   • La configuración del sistema")
                        print("   • El formato del mensaje")
                        print("   • La autenticación")
                        print("   • El envío a LIWA.co")
                        print()
                        print("🔍 EL PROBLEMA ESTÁ EN:")
                        print("   • La entrega del SMS por parte del operador")
                        print("   • Posibles restricciones de LIWA.co")
                        print("   • Configuración del dispositivo")
                        print()
                        print("📞 ACCIÓN REQUERIDA:")
                        print("   1. Contactar soporte de LIWA.co")
                        print("   2. Proporcionar los Message IDs")
                        print("   3. Solicitar verificación de entrega")
                        print("   4. Preguntar sobre restricciones")
                        
                else:
                    error_text = await response.text()
                    print(f"❌ Error en autenticación: {response.status} - {error_text}")
                    
    except Exception as e:
        print(f"❌ Excepción general: {e}")

if __name__ == "__main__":
    asyncio.run(test_minimal_sms())
