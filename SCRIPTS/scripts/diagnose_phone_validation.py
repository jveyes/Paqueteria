#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas con la validación de teléfonos
"""

import sys
import os
import requests
import json
import time
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def diagnose_phone_validation():
    """Diagnosticar problemas con la validación de teléfonos"""
    print("🔍 DIAGNÓSTICO DE VALIDACIÓN DE TELÉFONOS")
    print("=" * 70)
    
    base_url = "http://localhost"
    
    print("📋 DIAGNÓSTICO PASO A PASO:")
    print("=" * 50)
    
    # Paso 1: Verificar que la página esté funcionando
    print("\n1️⃣ VERIFICANDO PÁGINA DEL FORMULARIO...")
    try:
        response = requests.get(f"{base_url}/announce")
        if response.status_code == 200:
            print("   ✅ Página accesible")
            
            # Verificar elementos críticos
            html_content = response.text
            
            checks = [
                ("Función validatePhoneNumber", "function validatePhoneNumber"),
                ("Validación internacional", "phoneValidation = validatePhoneNumber"),
                ("Validación antigua (debe estar ausente)", "startsWith('3') && !phoneDigits.startsWith('6')"),
                ("Validación solo números (debe estar ausente)", "solo puede contener números"),
                ("Endpoint API", "api/announcements"),
                ("JavaScript", "fetch('/api/announcements/'"),
            ]
            
            for check_name, check_text in checks:
                if check_text in html_content:
                    if "debe estar ausente" in check_name:
                        print(f"   ❌ {check_name}: ENCONTRADO (NO DEBERÍA ESTAR)")
                    else:
                        print(f"   ✅ {check_name}: Encontrado")
                else:
                    if "debe estar ausente" in check_name:
                        print(f"   ✅ {check_name}: NO encontrado (CORRECTO)")
                    else:
                        print(f"   ❌ {check_name}: NO encontrado")
                    
        else:
            print(f"   ❌ Error accediendo a la página: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Paso 2: Verificar que la API esté funcionando
    print("\n2️⃣ VERIFICANDO API DE ANUNCIOS...")
    test_cases = [
        {
            "name": "Número internacional válido",
            "data": {
                "customer_name": "Test User",
                "guide_number": "TEST001",
                "customer_phone": "+13008103849"
            },
            "expected_status": 200
        },
        {
            "name": "Número colombiano válido",
            "data": {
                "customer_name": "Test User",
                "guide_number": "TEST002",
                "customer_phone": "3008103849"
            },
            "expected_status": 200
        },
        {
            "name": "Número con espacios (inválido)",
            "data": {
                "customer_name": "Test User",
                "guide_number": "TEST003",
                "customer_phone": "+1 300 810 3849"
            },
            "expected_status": 422
        },
        {
            "name": "Número sin código > 10 dígitos (inválido)",
            "data": {
                "customer_name": "Test User",
                "guide_number": "TEST004",
                "customer_phone": "13008103849"
            },
            "expected_status": 422
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(
                f"{base_url}/api/announcements/",
                headers={"Content-Type": "application/json"},
                json=test_case["data"]
            )
            
            if response.status_code == test_case["expected_status"]:
                print(f"   ✅ {test_case['name']}: {response.status_code} (CORRECTO)")
            else:
                print(f"   ❌ {test_case['name']}: {response.status_code} (ESPERADO: {test_case['expected_status']})")
                if response.status_code != 200:
                    try:
                        error_data = response.json()
                        print(f"      Error: {error_data}")
                    except:
                        print(f"      Error: {response.text}")
                        
        except Exception as e:
            print(f"   ❌ {test_case['name']}: Error - {e}")
    
    # Paso 3: Verificar timestamp del archivo
    print("\n3️⃣ VERIFICANDO ARCHIVOS...")
    try:
        announce_file = Path("CODE/templates/customers/announce.html")
        if announce_file.exists():
            stat = announce_file.stat()
            mod_time = time.ctime(stat.st_mtime)
            print(f"   ✅ announce.html: Modificado {mod_time}")
        else:
            print(f"   ❌ announce.html: NO ENCONTRADO")
            
        security_file = Path("CODE/src/utils/security.py")
        if security_file.exists():
            stat = security_file.stat()
            mod_time = time.ctime(stat.st_mtime)
            print(f"   ✅ security.py: Modificado {mod_time}")
        else:
            print(f"   ❌ security.py: NO ENCONTRADO")
            
    except Exception as e:
        print(f"   ❌ Error verificando archivos: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 DIAGNÓSTICO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    diagnose_phone_validation()
