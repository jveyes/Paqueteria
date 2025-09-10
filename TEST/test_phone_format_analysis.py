#!/usr/bin/env python3
"""
Análisis del formato de números de teléfono para LIWA.co
Verificar qué formato es el correcto
"""

import asyncio
import aiohttp
import json

async def test_phone_formats():
    """Probar diferentes formatos de número de teléfono"""
    print("📱 ANÁLISIS DE FORMATO DE NÚMEROS DE TELÉFONO")
    print("=" * 60)
    
    # Diferentes formatos del número 3002596319
    phone_formats = [
        "3002596319",      # 10 dígitos (formato actual)
        "573002596319",    # 12 dígitos con código país
        "+573002596319",   # Con signo +
        "300-259-6319",    # Con guiones
        "300 259 6319",    # Con espacios
    ]
    
    print("🔍 FORMATOS A PROBAR:")
    for i, phone in enumerate(phone_formats, 1):
        print(f"   {i}. {phone}")
    print()
    
    # Datos de prueba
    test_data = {
        "customer_name": "PRUEBA FORMATO",
        "guide_number": "FORMAT123",
        "tracking_code": "FMT1"
    }
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        for i, phone in enumerate(phone_formats, 1):
            print(f"📞 PROBANDO FORMATO {i}: {phone}")
            
            # Limpiar el número para el payload
            clean_phone = ''.join(filter(str.isdigit, phone))
            test_data["customer_phone"] = clean_phone
            
            try:
                # Simular envío desde navegador
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
                        print(f"   ✅ ÉXITO: {result.get('message', 'SMS enviado')}")
                        print(f"   📱 Número procesado: {result.get('phone', 'N/A')}")
                        results.append({
                            "format": phone,
                            "clean": clean_phone,
                            "success": True,
                            "processed_phone": result.get('phone', 'N/A')
                        })
                    else:
                        error_text = await response.text()
                        print(f"   ❌ ERROR: {response.status} - {error_text}")
                        results.append({
                            "format": phone,
                            "clean": clean_phone,
                            "success": False,
                            "error": error_text
                        })
                        
            except Exception as e:
                print(f"   ❌ EXCEPCIÓN: {e}")
                results.append({
                    "format": phone,
                    "clean": clean_phone,
                    "success": False,
                    "error": str(e)
                })
            
            print()
            
            # Esperar entre pruebas
            await asyncio.sleep(2)
    
    # Resumen de resultados
    print("=" * 60)
    print("📊 RESUMEN DE RESULTADOS:")
    print("=" * 60)
    
    for result in results:
        status = "✅ ÉXITO" if result["success"] else "❌ FALLÓ"
        print(f"{status} | {result['format']} → {result['clean']}")
        if result["success"]:
            print(f"        Procesado como: {result['processed_phone']}")
        else:
            print(f"        Error: {result.get('error', 'N/A')}")
        print()
    
    # Análisis
    successful_formats = [r for r in results if r["success"]]
    
    if successful_formats:
        print("🎯 FORMATOS EXITOSOS:")
        for result in successful_formats:
            print(f"   • {result['format']} → {result['processed_phone']}")
        
        print("\n💡 RECOMENDACIÓN:")
        print("   Usa el formato que funcione mejor para tu número.")
        print("   Revisa tu teléfono para ver cuál SMS llegó correctamente.")
    else:
        print("❌ NINGÚN FORMATO FUNCIONÓ")
        print("   Revisar configuración de LIWA.co o conectividad")
    
    print("\n🔍 PRÓXIMOS PASOS:")
    print("   1. Revisar logs: docker-compose logs app | grep SMS")
    print("   2. Verificar número de teléfono real")
    print("   3. Contactar soporte LIWA.co si es necesario")

if __name__ == "__main__":
    asyncio.run(test_phone_formats())
