#!/usr/bin/env python3
"""
Script para verificar que la corrección del display del teléfono funciona
"""

import requests
import json

def test_dashboard_phone_display():
    """Probar que el dashboard muestre correctamente los teléfonos"""
    
    print("🔍 Probando display de teléfonos en dashboard...")
    print("=" * 60)
    
    try:
        # Hacer petición al dashboard
        response = requests.get("http://localhost/dashboard", timeout=10)
        
        if response.status_code == 200:
            print("✅ Dashboard accesible")
            
            # Buscar patrones de teléfono en el HTML
            html_content = response.text
            
            # Buscar "Sin teléfono" en el HTML
            sin_telefono_count = html_content.count("Sin teléfono")
            print(f"📊 Ocurrencias de 'Sin teléfono': {sin_telefono_count}")
            
            # Buscar números de teléfono específicos
            phone_patterns = ["3002596319", "3008103849", "3128432422", "3024546729"]
            for pattern in phone_patterns:
                count = html_content.count(pattern)
                print(f"📱 Ocurrencias de '{pattern}': {count}")
            
            # Buscar el patrón problemático
            undefined_count = html_content.count("undefined")
            print(f"❌ Ocurrencias de 'undefined': {undefined_count}")
            
            # Mostrar fragmentos relevantes del HTML
            print(f"\n🔍 Fragmentos del HTML que contienen teléfonos:")
            lines = html_content.split('\n')
            for i, line in enumerate(lines):
                if 'customer_phone' in line or 'Sin teléfono' in line or '3002596319' in line:
                    print(f"  Línea {i+1}: {line.strip()}")
            
        else:
            print(f"❌ Error accediendo al dashboard: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_announcement_detail_phone_display():
    """Probar que la vista de detalles muestre correctamente los teléfonos"""
    
    print("\n🔍 Probando display de teléfonos en vista de detalles...")
    print("=" * 60)
    
    # Códigos de prueba
    test_codes = ["DSVS", "N61P", "BBFV"]
    
    for code in test_codes:
        print(f"\n📦 Probando código: {code}")
        
        try:
            # Hacer petición a la vista de detalles
            response = requests.get(f"http://localhost/announcements/guide/{code}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Vista de detalles accesible para {code}")
                
                html_content = response.text
                
                # Buscar patrones de teléfono
                sin_telefono_count = html_content.count("Sin teléfono")
                print(f"  📊 Ocurrencias de 'Sin teléfono': {sin_telefono_count}")
                
                # Buscar números de teléfono
                phone_found = False
                for pattern in ["3002596319", "3008103849", "3128432422", "3024546729"]:
                    if pattern in html_content:
                        print(f"  📱 Número encontrado: {pattern}")
                        phone_found = True
                
                if not phone_found:
                    print(f"  ⚠️ No se encontraron números de teléfono")
                
                # Buscar undefined
                undefined_count = html_content.count("undefined")
                if undefined_count > 0:
                    print(f"  ❌ Ocurrencias de 'undefined': {undefined_count}")
                
            elif response.status_code == 404:
                print(f"❌ Anuncio {code} no encontrado")
            else:
                print(f"❌ Error accediendo a {code}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error probando {code}: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando prueba de display de teléfonos")
    
    # Probar dashboard
    test_dashboard_phone_display()
    
    # Probar vista de detalles
    test_announcement_detail_phone_display()
    
    print("\n🏁 Prueba completada")
