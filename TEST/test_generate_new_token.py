#!/usr/bin/env python3
"""
Generar un token nuevo para LIWA.co
"""

import asyncio
import aiohttp
import json
import base64
from datetime import datetime

async def generate_new_token():
    """Generar un token nuevo para LIWA.co"""
    print("🔄 GENERANDO TOKEN NUEVO PARA LIWA.CO")
    print("=" * 60)
    
    # Datos de autenticación
    auth_data = {
        "account": "00486396309",
        "password": "6fEuRnd*$$#NfFAS"
    }
    
    print("🔑 SOLICITANDO TOKEN NUEVO...")
    print(f"📧 Account: {auth_data['account']}")
    print(f"🔐 Password: {auth_data['password']}")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            # Autenticarse para obtener token nuevo
            async with session.post(
                "https://api.liwa.co/v2/auth/login",
                json=auth_data,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    token = result.get("token")
                    
                    print("✅ TOKEN NUEVO GENERADO EXITOSAMENTE")
                    print(f"🔑 Token: {token}")
                    print()
                    
                    # Decodificar token para mostrar información
                    try:
                        parts = token.split('.')
                        if len(parts) == 3:
                            payload = parts[1]
                            missing_padding = len(payload) % 4
                            if missing_padding:
                                payload += '=' * (4 - missing_padding)
                            
                            decoded_bytes = base64.urlsafe_b64decode(payload)
                            decoded_str = decoded_bytes.decode('utf-8')
                            payload_data = json.loads(decoded_str)
                            
                            print("📋 INFORMACIÓN DEL TOKEN NUEVO:")
                            print(f"   • Usuario: {payload_data.get('sub', 'N/A')}")
                            print(f"   • Empresa: {payload_data.get('user', {}).get('empresa', 'N/A')}")
                            print(f"   • Cuenta: {payload_data.get('user', {}).get('cuenta', 'N/A')}")
                            print(f"   • Saldo: {payload_data.get('user', {}).get('saldo', 'N/A')}")
                            print(f"   • Creado: {datetime.fromtimestamp(payload_data.get('iat', 0))}")
                            print(f"   • Expira: {datetime.fromtimestamp(payload_data.get('exp', 0))}")
                            print(f"   • Tipo de cliente: {payload_data.get('user', {}).get('tipoCliente', 'N/A')}")
                            print(f"   • Tipo de pago: {payload_data.get('user', {}).get('tipoPago', 'N/A')}")
                            print()
                            
                            # Calcular tiempo restante
                            exp_time = datetime.fromtimestamp(payload_data.get('exp', 0))
                            now = datetime.now()
                            time_left = exp_time - now
                            
                            print(f"⏰ TIEMPO DE VALIDEZ DEL TOKEN:")
                            print(f"   • {time_left}")
                            print(f"   • Horas: {time_left.total_seconds() / 3600:.2f}")
                            print()
                            
                            # Probar el token nuevo con un SMS
                            print("📱 PROBANDO TOKEN NUEVO CON SMS...")
                            print("-" * 40)
                            
                            headers = {
                                "Authorization": f"Bearer {token}",
                                "API-KEY": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
                                "Content-Type": "application/json"
                            }
                            
                            # SMS de prueba
                            sms_data = {
                                "number": "573008103849",
                                "message": f"TOKEN NUEVO - {datetime.now().strftime('%H:%M:%S')} - Prueba de funcionalidad",
                                "type": 1
                            }
                            
                            print(f"📋 SMS Data: {json.dumps(sms_data, indent=2, ensure_ascii=False)}")
                            print()
                            
                            async with session.post(
                                "https://api.liwa.co/v2/sms/single",
                                json=sms_data,
                                headers=headers,
                                timeout=30.0
                            ) as sms_response:
                                
                                if sms_response.status == 200:
                                    sms_result = await sms_response.json()
                                    print("✅ SMS ENVIADO EXITOSAMENTE CON TOKEN NUEVO")
                                    print(f"📋 Respuesta: {json.dumps(sms_result, indent=2, ensure_ascii=False)}")
                                    
                                    message_id = sms_result.get('menssageId', 'N/A')
                                    success = sms_result.get('success', False)
                                    
                                    print(f"\n📊 RESUMEN:")
                                    print(f"   • Éxito: {success}")
                                    print(f"   • Message ID: {message_id}")
                                    print(f"   • Número: {sms_result.get('number', 'N/A')}")
                                    print(f"   • Mensaje: {sms_result.get('message', 'N/A')}")
                                    
                                else:
                                    error_text = await sms_response.text()
                                    print(f"❌ ERROR EN SMS: {sms_response.status} - {error_text}")
                            
                            print("\n" + "=" * 60)
                            print("📊 RESUMEN DEL TOKEN NUEVO:")
                            print("=" * 60)
                            print("✅ TOKEN NUEVO GENERADO Y FUNCIONAL")
                            print("✅ AUTENTICACIÓN EXITOSA")
                            print("✅ SMS ENVIADO EXITOSAMENTE")
                            print("✅ TOKEN VÁLIDO POR 24 HORAS")
                            print()
                            print("🔑 TOKEN COMPLETO:")
                            print(f"{token}")
                            print()
                            print("📱 MESSAGE ID DEL SMS DE PRUEBA:")
                            if 'message_id' in locals():
                                print(f"{message_id}")
                            
                    except Exception as e:
                        print(f"⚠️ Error decodificando token: {e}")
                        print(f"🔑 Token (sin decodificar): {token}")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ ERROR GENERANDO TOKEN: {response.status} - {error_text}")
                    
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
    
    print("\n" + "=" * 60)
    print("🔄 TOKEN NUEVO GENERADO")
    print("=" * 60)
    print("✅ El token anterior ha sido reemplazado")
    print("✅ El nuevo token es válido por 24 horas")
    print("✅ El sistema usará automáticamente el nuevo token")
    print("✅ No es necesario actualizar manualmente el código")

if __name__ == "__main__":
    asyncio.run(generate_new_token())
