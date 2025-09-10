#!/usr/bin/env python3
"""
Script para debuggear el endpoint de búsqueda y verificar por qué customer_phone aparece como undefined
"""

import requests
import json
import sys

def test_search_endpoint():
    """Probar el endpoint de búsqueda con diferentes códigos"""
    
    base_url = "http://localhost"
    
    # Códigos de prueba conocidos
    test_codes = [
        "YJWX",  # Código de tracking conocido
        "Z7UH",  # Otro código de tracking
        "12345", # Número de guía de prueba
    ]
    
    print("🔍 Probando endpoint de búsqueda...")
    print("=" * 60)
    
    for code in test_codes:
        print(f"\n📦 Probando código: {code}")
        print("-" * 40)
        
        try:
            # Hacer la petición al endpoint
            url = f"{base_url}/api/announcements/search/package"
            params = {"query": code}
            
            response = requests.get(url, params=params, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ Respuesta exitosa:")
                print(f"  - customer_name: {data.get('announcement', {}).get('customer_name', 'NO ENCONTRADO')}")
                print(f"  - customer_phone: {data.get('announcement', {}).get('customer_phone', 'NO ENCONTRADO')}")
                print(f"  - guide_number: {data.get('announcement', {}).get('guide_number', 'NO ENCONTRADO')}")
                print(f"  - tracking_code: {data.get('announcement', {}).get('tracking_code', 'NO ENCONTRADO')}")
                
                # Verificar estructura completa
                print("\n📋 Estructura completa del announcement:")
                announcement = data.get('announcement', {})
                for key, value in announcement.items():
                    print(f"  - {key}: {value} (tipo: {type(value).__name__})")
                
                # Verificar si hay datos en package
                package = data.get('package', {})
                if package:
                    print("\n📦 Datos del package:")
                    for key, value in package.items():
                        print(f"  - {key}: {value} (tipo: {type(value).__name__})")
                
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
    
    print("\n" + "=" * 60)
    print("🏁 Prueba completada")

def test_database_direct():
    """Probar consulta directa a la base de datos"""
    print("\n🔍 Probando consulta directa a la base de datos...")
    
    try:
        # Importar dependencias
        import os
        import sys
        
        # Agregar el directorio del proyecto al path
        project_root = "/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code"
        sys.path.insert(0, project_root)
        
        from src.database.database import get_db
        from src.models.announcement import PackageAnnouncement
        from sqlalchemy.orm import Session
        
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Consultar algunos anuncios
        announcements = db.query(PackageAnnouncement).limit(5).all()
        
        print(f"📊 Encontrados {len(announcements)} anuncios:")
        
        for announcement in announcements:
            print(f"\n📦 Anuncio {announcement.tracking_code}:")
            print(f"  - ID: {announcement.id}")
            print(f"  - customer_name: {announcement.customer_name}")
            print(f"  - customer_phone: {announcement.customer_phone}")
            print(f"  - guide_number: {announcement.guide_number}")
            print(f"  - tracking_code: {announcement.tracking_code}")
            print(f"  - is_active: {announcement.is_active}")
            print(f"  - is_processed: {announcement.is_processed}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error consultando base de datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando debug del endpoint de búsqueda")
    
    # Probar endpoint
    test_search_endpoint()
    
    # Probar base de datos
    test_database_direct()
