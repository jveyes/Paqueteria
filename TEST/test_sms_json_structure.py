#!/usr/bin/env python3
"""
Mostrar la estructura JSON del envío de SMS y probar con nuevo número
"""

import asyncio
import aiohttp
import json

async def test_sms_json_structure():
    """Mostrar estructura JSON y probar con nuevo número"""
    print("📱 ESTRUCTURA JSON DEL ENVÍO DE SMS")
    print("=" * 60)
    
    # Datos de prueba
    test_data = {
        "customer_name": "PRUEBA JSON",
        "guide_number": "JSON123",
        "tracking_code": "J1"
    }
    
    print("🔍 ESTRUCTURA DEL JSON QUE SE ENVÍA A LIWA.CO:")
    print("-" * 40)
    
    # Simular la construcción del JSON como lo hace el código
    customer_name = test_data["customer_name"]
    guide_number = test_data["guide_number"]
    tracking_code = test_data["tracking_code"]
    
    # Construir mensaje (igual que en el código)
    message = (
        f"Hola {customer_name}, tu paquete con guía {guide_number} "
        f"ha sido registrado. Código de consulta: {tracking_code}. "
        f"PAQUETES EL CLUB"
    )
    
    # Formatear número (igual que en el código)
    phone = "3008103849"  # Nuevo número
    clean_phone = ''.join(filter(str.isdigit, phone))
    
    if len(clean_phone) == 10:
        if not clean_phone.startswith(('3', '6')):
            raise ValueError("El número debe ser un celular o fijo colombiano válido")
        formatted_phone = f"57{clean_phone}"
    else:
        formatted_phone = clean_phone
    
    # Estructura del JSON que se envía a LIWA.co
    sms_data = {
        "number": formatted_phone,
        "message": message,
        "type": 1  # SMS estándar
    }
    
    print("📋 JSON ENVIADO A LIWA.CO:")
    print(json.dumps(sms_data, indent=2, ensure_ascii=False))
    print()
    
    print("🔑 HEADERS ENVIADOS:")
    headers = {
        "Authorization": "Bearer [TOKEN_JWT]",
        "API-KEY": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
        "Content-Type": "application/json"
    }
    print(json.dumps(headers, indent=2))
    print()
    
    print("🌐 URL DE DESTINO:")
    print("POST https://api.liwa.co/v2/sms/single")
    print()
    
    print("=" * 60)
    print("📱 PROBANDO ENVÍO CON NUEVO NÚMERO")
    print("=" * 60)
    
    # Probar con el nuevo número
    test_data["customer_phone"] = "3008103849"
    
    print(f"📞 Número original: {test_data['customer_phone']}")
    print(f"📞 Número formateado: {formatted_phone}")
    print(f"👤 Cliente: {test_data['customer_name']}")
    print(f"📦 Guía: {test_data['guide_number']}")
    print(f"🔑 Tracking: {test_data['tracking_code']}")
    print(f"📝 Mensaje: {message}")
    print()
    
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            print("📤 ENVIANDO SMS...")
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
                    
                    # Mostrar respuesta completa de LIWA.co
                    liwa_response = result.get('liwa_response', {})
                    if liwa_response:
                        print(f"🌐 RESPUESTA DE LIWA.CO:")
                        print(json.dumps(liwa_response, indent=2, ensure_ascii=False))
                        
                        # Extraer información importante
                        message_id = liwa_response.get('menssageId', 'N/A')
                        success = liwa_response.get('success', False)
                        liwa_message = liwa_response.get('message', 'N/A')
                        liwa_number = liwa_response.get('number', 'N/A')
                        
                        print(f"\n📊 RESUMEN:")
                        print(f"   • Éxito: {success}")
                        print(f"   • Message ID: {message_id}")
                        print(f"   • Mensaje LIWA: {liwa_message}")
                        print(f"   • Número LIWA: {liwa_number}")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ ERROR: {response.status} - {error_text}")
                    
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 VERIFICACIÓN DE LOGS:")
    print("=" * 60)
    print("Revisa los logs para confirmar el envío:")
    print("   docker-compose logs app | grep -i 'sms\|liwa\|3008103849' | tail -10")
    print()
    print("📱 INSTRUCCIONES PARA VERIFICAR:")
    print("   1. Revisa tu teléfono 3008103849")
    print("   2. Busca en todas las carpetas de mensajes")
    print("   3. Verifica si hay filtros activos")
    print("   4. Espera hasta 15 minutos (puede haber retraso)")

if __name__ == "__main__":
    asyncio.run(test_sms_json_structure())
