#!/usr/bin/env python3
"""
Script para simular exactamente el endpoint del dashboard
"""

import sys
import os
import requests
from datetime import datetime

# Agregar el directorio del proyecto al path
project_root = "/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code"
sys.path.insert(0, project_root)

from src.database.database import get_db
from src.models.announcement import PackageAnnouncement
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

def simulate_dashboard_endpoint():
    """Simular exactamente el endpoint del dashboard"""
    
    print("🔍 Simulando endpoint del dashboard...")
    print("=" * 60)
    
    try:
        # Simular la lógica exacta del dashboard
        db = next(get_db())
        
        # Estadísticas de anuncios por estado
        announced_packages = db.query(PackageAnnouncement).filter(
            and_(PackageAnnouncement.is_active == True, PackageAnnouncement.is_processed == False)
        ).count()
        
        received_packages = db.query(PackageAnnouncement).filter(
            and_(PackageAnnouncement.is_active == True, PackageAnnouncement.is_processed == True)
        ).count()
        
        delivered_packages = db.query(PackageAnnouncement).filter(
            and_(PackageAnnouncement.is_active == True, PackageAnnouncement.is_processed == True)
        ).count()
        
        # Anuncios recientes (últimos 10) - ordenados por fecha de anuncio
        recent_packages = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_active == True
        ).order_by(desc(PackageAnnouncement.announced_at)).limit(10).all()
        
        print(f"📊 Estadísticas:")
        print(f"  - announced_packages: {announced_packages}")
        print(f"  - received_packages: {received_packages}")
        print(f"  - delivered_packages: {delivered_packages}")
        print(f"  - recent_packages count: {len(recent_packages)}")
        
        print(f"\n📦 Paquetes recientes:")
        for i, package in enumerate(recent_packages):
            print(f"  {i+1}. {package.tracking_code} - {package.customer_name} - {package.customer_phone}")
            
            # Verificar si el problema está en el objeto
            if hasattr(package, 'customer_phone'):
                print(f"     - hasattr(customer_phone): True")
                print(f"     - customer_phone value: {repr(package.customer_phone)}")
                print(f"     - customer_phone type: {type(package.customer_phone)}")
            else:
                print(f"     - hasattr(customer_phone): False")
            
            # Verificar si el problema está en la serialización
            try:
                # Simular lo que hace Jinja2
                phone_value = package.customer_phone if package.customer_phone else 'Sin teléfono'
                print(f"     - template evaluation: {repr(phone_value)}")
            except Exception as e:
                print(f"     - template evaluation error: {e}")
        
        # Probar la serialización del objeto completo
        print(f"\n🔍 Probando serialización del objeto:")
        try:
            # Simular lo que hace FastAPI al pasar el objeto al template
            package_dict = {
                'id': str(package.id),
                'customer_name': package.customer_name,
                'customer_phone': package.customer_phone,
                'guide_number': package.guide_number,
                'tracking_code': package.tracking_code,
                'is_active': package.is_active,
                'is_processed': package.is_processed,
                'announced_at': package.announced_at
            }
            print(f"  - package_dict: {package_dict}")
        except Exception as e:
            print(f"  - Error creando dict: {e}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_direct_template_access():
    """Probar acceso directo al template"""
    
    print("\n🔍 Probando acceso directo al template...")
    print("=" * 60)
    
    try:
        # Hacer petición directa al dashboard
        response = requests.get("http://localhost/dashboard", timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Buscar líneas específicas que contengan customer_phone
            lines = html_content.split('\n')
            for i, line in enumerate(lines):
                if 'customer_phone' in line or 'Sin teléfono' in line:
                    print(f"  Línea {i+1}: {line.strip()}")
            
            # Buscar el patrón específico del template
            print(f"\n🔍 Buscando patrones específicos:")
            for i, line in enumerate(lines):
                if 'package.customer_phone' in line:
                    print(f"  Línea {i+1}: {line.strip()}")
                elif 'announcement.customer_phone' in line:
                    print(f"  Línea {i+1}: {line.strip()}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando simulación del endpoint del dashboard")
    
    # Simular endpoint
    simulate_dashboard_endpoint()
    
    # Probar acceso directo
    test_direct_template_access()
    
    print("\n🏁 Simulación completada")
