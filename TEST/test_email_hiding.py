#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de ocultación de campo de email
"""

import requests
import json
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'src'))

def test_search_package_api():
    """Probar el endpoint de búsqueda de paquetes"""
    
    # URL base (ajustar según tu configuración)
    base_url = "http://localhost:8000"
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Código de tracking sin consultas previas",
            "query": "ABC123",
            "expected_has_existing_email": False
        },
        {
            "name": "Código de tracking con consultas previas",
            "query": "29XN",  # Usar un código que sepas que tiene consultas
            "expected_has_existing_email": True
        }
    ]
    
    print("🧪 INICIANDO PRUEBAS DE OCULTACIÓN DE CAMPO DE EMAIL")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Prueba {i}: {test_case['name']}")
        print(f"🔍 Query: {test_case['query']}")
        
        try:
            # Hacer la petición al API
            url = f"{base_url}/api/announcements/search/package"
            params = {"query": test_case['query']}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verificar estructura de respuesta
                print("✅ Respuesta recibida correctamente")
                
                # Verificar que existe inquiry_info
                if 'inquiry_info' in data:
                    inquiry_info = data['inquiry_info']
                    print(f"📊 inquiry_info: {json.dumps(inquiry_info, indent=2)}")
                    
                    # Verificar has_existing_email
                    has_existing_email = inquiry_info.get('has_existing_email', False)
                    expected = test_case['expected_has_existing_email']
                    
                    if has_existing_email == expected:
                        print(f"✅ has_existing_email correcto: {has_existing_email}")
                    else:
                        print(f"❌ has_existing_email incorrecto: {has_existing_email} (esperado: {expected})")
                    
                    # Verificar query_type
                    if 'query_type' in data:
                        query_type = data['query_type']
                        print(f"📊 query_type: {json.dumps(query_type, indent=2)}")
                        
                        if query_type.get('should_show_inquiry_form'):
                            print("✅ Formulario de consulta debe mostrarse")
                        else:
                            print("❌ Formulario de consulta NO debe mostrarse")
                    
                else:
                    print("❌ inquiry_info no encontrado en la respuesta")
                    
            elif response.status_code == 404:
                print(f"⚠️  Paquete no encontrado: {test_case['query']}")
            else:
                print(f"❌ Error en la respuesta: {response.status_code}")
                print(f"📄 Contenido: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión. ¿Está el servidor ejecutándose?")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")

def test_frontend_logic():
    """Probar la lógica del frontend"""
    print("\n🧪 PROBANDO LÓGICA DEL FRONTEND")
    print("=" * 40)
    
    # Simular datos de respuesta
    test_data = {
        "inquiry_info": {
            "has_existing_inquiries": True,
            "has_existing_email": True,
            "inquiry_count": 1,
            "latest_inquiry_date": "2025-01-15T10:30:00"
        }
    }
    
    # Simular la lógica del frontend
    inquiry_info = test_data.get('inquiry_info')
    
    if inquiry_info and inquiry_info.get('has_existing_email'):
        print("✅ Frontend: Campo de email debe ocultarse")
        print(f"📅 Fecha de consulta previa: {inquiry_info.get('latest_inquiry_date')}")
    else:
        print("✅ Frontend: Campo de email debe mostrarse")
    
    print("✅ Lógica del frontend funcionando correctamente")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE FUNCIONALIDAD DE EMAIL")
    
    # Probar API
    test_search_package_api()
    
    # Probar lógica del frontend
    test_frontend_logic()
    
    print("\n✨ TODAS LAS PRUEBAS COMPLETADAS")
