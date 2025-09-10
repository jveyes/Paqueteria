#!/usr/bin/env python3
"""
Script para simular exactamente lo que hace el navegador al buscar un paquete
"""

import requests
import json
import time

def simulate_browser_search():
    """Simular búsqueda desde el navegador"""
    
    base_url = "http://localhost"
    test_code = "29XN"  # Código conocido
    
    print("🌐 Simulando búsqueda desde navegador...")
    print("=" * 60)
    
    # Headers que simula un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': f'{base_url}/search'
    }
    
    try:
        # Hacer la petición exactamente como lo haría el navegador
        url = f"{base_url}/api/announcements/search/package"
        params = {"query": test_code}
        
        print(f"🔗 URL: {url}")
        print(f"📋 Parámetros: {params}")
        print(f"📋 Headers: {headers}")
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"📡 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✅ Datos recibidos:")
            print(f"  - Tipo de respuesta: {type(data)}")
            print(f"  - Claves principales: {list(data.keys())}")
            
            # Verificar estructura del announcement
            announcement = data.get('announcement', {})
            print(f"\n📦 Estructura del announcement:")
            print(f"  - Claves: {list(announcement.keys())}")
            print(f"  - customer_name: {repr(announcement.get('customer_name'))}")
            print(f"  - customer_phone: {repr(announcement.get('customer_phone'))}")
            print(f"  - guide_number: {repr(announcement.get('guide_number'))}")
            print(f"  - tracking_code: {repr(announcement.get('tracking_code'))}")
            
            # Verificar tipos
            customer_phone = announcement.get('customer_phone')
            print(f"\n🔍 Análisis de customer_phone:")
            print(f"  - Valor: {repr(customer_phone)}")
            print(f"  - Tipo: {type(customer_phone).__name__}")
            print(f"  - Es None: {customer_phone is None}")
            print(f"  - Es undefined (string): {customer_phone == 'undefined'}")
            print(f"  - Es string vacío: {customer_phone == ''}")
            print(f"  - Longitud: {len(str(customer_phone)) if customer_phone is not None else 'N/A'}")
            
            # Simular el JavaScript del frontend
            print(f"\n🎯 Simulando JavaScript del frontend:")
            
            # Simular document.getElementById
            customer_phone_element = {
                'textContent': None,
                'id': 'customerPhone'
            }
            
            # Simular la asignación del JavaScript
            if customer_phone_element:
                print(f"  - Elemento customerPhone encontrado: {customer_phone_element['id']}")
                print(f"  - Asignando textContent: {repr(customer_phone)}")
                customer_phone_element['textContent'] = customer_phone
                print(f"  - textContent después de asignar: {repr(customer_phone_element['textContent'])}")
                
                # Verificar si aparece como "undefined"
                if str(customer_phone_element['textContent']) == 'undefined':
                    print(f"  ❌ PROBLEMA DETECTADO: textContent es 'undefined'")
                else:
                    print(f"  ✅ textContent correcto: {repr(customer_phone_element['textContent'])}")
            
            # Mostrar respuesta completa para análisis
            print(f"\n📄 Respuesta completa (JSON):")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

def test_different_codes():
    """Probar con diferentes códigos para ver si el problema es específico"""
    
    base_url = "http://localhost"
    test_codes = ["29XN", "8M2S", "XJQZ"]
    
    print("\n🔍 Probando múltiples códigos...")
    print("=" * 60)
    
    for code in test_codes:
        print(f"\n📦 Probando código: {code}")
        print("-" * 40)
        
        try:
            url = f"{base_url}/api/announcements/search/package"
            params = {"query": code}
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                announcement = data.get('announcement', {})
                customer_phone = announcement.get('customer_phone')
                
                print(f"  - customer_phone: {repr(customer_phone)}")
                print(f"  - tipo: {type(customer_phone).__name__}")
                print(f"  - es undefined: {customer_phone == 'undefined'}")
                
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando simulación de navegador")
    
    # Simular búsqueda desde navegador
    simulate_browser_search()
    
    # Probar múltiples códigos
    test_different_codes()
    
    print("\n🏁 Simulación completada")
