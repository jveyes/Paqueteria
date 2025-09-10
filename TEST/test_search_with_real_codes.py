#!/usr/bin/env python3
"""
Script para probar el endpoint de búsqueda con códigos reales de la base de datos
"""

import requests
import json

def test_search_with_real_codes():
    """Probar el endpoint de búsqueda con códigos reales"""
    
    base_url = "http://localhost"
    
    # Códigos reales de la base de datos
    real_codes = [
        "29XN",  # JESUS VILLALOBOS - 3002596319
        "8M2S",  # ANGELICA ARRAZOLA - 3008103849
        "XJQZ",  # LAIS HERNANDEZ - 3128432422
        "S9FR",  # RAFAEL CABARCAS - 3024546729
        "J7IC",  # JESUS MARIA VILLALOBOS - 3002596319
    ]
    
    print("🔍 Probando endpoint de búsqueda con códigos reales...")
    print("=" * 70)
    
    for code in real_codes:
        print(f"\n📦 Probando código: {code}")
        print("-" * 50)
        
        try:
            # Hacer la petición al endpoint
            url = f"{base_url}/api/announcements/search/package"
            params = {"query": code}
            
            response = requests.get(url, params=params, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ Respuesta exitosa:")
                announcement = data.get('announcement', {})
                
                print(f"  - customer_name: '{announcement.get('customer_name', 'NO ENCONTRADO')}'")
                print(f"  - customer_phone: '{announcement.get('customer_phone', 'NO ENCONTRADO')}'")
                print(f"  - guide_number: '{announcement.get('guide_number', 'NO ENCONTRADO')}'")
                print(f"  - tracking_code: '{announcement.get('tracking_code', 'NO ENCONTRADO')}'")
                
                # Verificar tipos de datos
                customer_phone = announcement.get('customer_phone')
                print(f"  - customer_phone tipo: {type(customer_phone).__name__}")
                print(f"  - customer_phone es None: {customer_phone is None}")
                print(f"  - customer_phone es string vacío: {customer_phone == ''}")
                
                # Verificar si hay datos en package
                package = data.get('package', {})
                if package:
                    print(f"\n📦 Datos del package:")
                    print(f"  - customer_phone: '{package.get('customer_phone', 'NO ENCONTRADO')}'")
                
                # Mostrar estructura completa del announcement
                print(f"\n📋 Estructura completa del announcement:")
                for key, value in announcement.items():
                    print(f"  - {key}: {repr(value)} (tipo: {type(value).__name__})")
                
            elif response.status_code == 404:
                print("❌ Paquete no encontrado")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Error decodificando JSON: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    print("\n" + "=" * 70)
    print("🏁 Prueba completada")

if __name__ == "__main__":
    test_search_with_real_codes()
