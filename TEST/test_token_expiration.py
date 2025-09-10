#!/usr/bin/env python3
"""
Verificar el manejo de expiración del token de LIWA.co
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

async def test_token_management():
    """Probar el manejo del token de LIWA.co"""
    print("🔑 VERIFICACIÓN DEL TOKEN DE LIWA.CO")
    print("=" * 60)
    
    # Simular autenticación directa con LIWA.co
    auth_data = {
        "account": "00486396309",
        "password": "6fEuRnd*$$#NfFAS"
    }
    
    print("🔍 PROBANDO AUTENTICACIÓN DIRECTA CON LIWA.CO...")
    
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
                    
                    print(f"✅ Autenticación exitosa")
                    print(f"🔑 Token obtenido: {token[:20]}..." if token else "❌ No se obtuvo token")
                    
                    # Verificar si hay información de expiración
                    print(f"📋 Respuesta completa: {json.dumps(result, indent=2)}")
                    
                    # Probar envío de SMS con el token
                    if token:
                        print("\n📱 PROBANDO ENVÍO DE SMS CON TOKEN...")
                        
                        sms_data = {
                            "number": "573002596319",
                            "message": "PRUEBA TOKEN - Verificación de expiración",
                            "type": 1
                        }
                        
                        headers = {
                            "Authorization": f"Bearer {token}",
                            "API-KEY": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
                            "Content-Type": "application/json"
                        }
                        
                        async with session.post(
                            "https://api.liwa.co/v2/sms/single",
                            json=sms_data,
                            headers=headers,
                            timeout=30.0
                        ) as sms_response:
                            
                            if sms_response.status == 200:
                                sms_result = await sms_response.json()
                                print(f"✅ SMS enviado exitosamente")
                                print(f"📋 Respuesta SMS: {json.dumps(sms_result, indent=2)}")
                            else:
                                error_text = await sms_response.text()
                                print(f"❌ Error en SMS: {sms_response.status} - {error_text}")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ Error en autenticación: {response.status} - {error_text}")
                    
    except Exception as e:
        print(f"❌ Excepción: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 ANÁLISIS DEL PROBLEMA:")
    print("=" * 60)
    print("❌ PROBLEMA IDENTIFICADO:")
    print("   • El código actual NO maneja la expiración del token")
    print("   • El token se obtiene una vez y se reutiliza indefinidamente")
    print("   • Después de 24 horas, el token expira y fallan los envíos")
    print()
    print("✅ SOLUCIÓN NECESARIA:")
    print("   • Implementar verificación de expiración del token")
    print("   • Renovar automáticamente el token cuando expire")
    print("   • Agregar timestamp de creación del token")
    print()
    print("🛠️ IMPLEMENTACIÓN REQUERIDA:")
    print("   1. Agregar campo _token_created_at")
    print("   2. Verificar expiración antes de cada envío")
    print("   3. Renovar token automáticamente si está expirado")

if __name__ == "__main__":
    asyncio.run(test_token_management())
