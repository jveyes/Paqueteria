#!/usr/bin/env python3
"""
Script para verificar qué datos se están pasando al dashboard
"""

import sys
import os

# Agregar el directorio del proyecto al path
project_root = "/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code"
sys.path.insert(0, project_root)

from src.database.database import get_db
from src.models.announcement import PackageAnnouncement
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

def test_dashboard_data():
    """Probar los datos que se pasan al dashboard"""
    
    print("🔍 Verificando datos del dashboard...")
    print("=" * 60)
    
    try:
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Simular la consulta del dashboard
        recent_packages = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_active == True
        ).order_by(desc(PackageAnnouncement.announced_at)).limit(5).all()
        
        print(f"📊 Encontrados {len(recent_packages)} paquetes recientes:")
        
        for i, package in enumerate(recent_packages):
            print(f"\n📦 Paquete {i+1}:")
            print(f"  - ID: {package.id}")
            print(f"  - customer_name: {package.customer_name}")
            print(f"  - customer_phone: {package.customer_phone}")
            print(f"  - guide_number: {package.guide_number}")
            print(f"  - tracking_code: {package.tracking_code}")
            print(f"  - is_active: {package.is_active}")
            print(f"  - is_processed: {package.is_processed}")
            print(f"  - announced_at: {package.announced_at}")
            
            # Verificar si customer_phone es None o vacío
            if package.customer_phone is None:
                print(f"  ❌ PROBLEMA: customer_phone es None")
            elif package.customer_phone == '':
                print(f"  ❌ PROBLEMA: customer_phone es string vacío")
            elif package.customer_phone == 'undefined':
                print(f"  ❌ PROBLEMA: customer_phone es 'undefined'")
            else:
                print(f"  ✅ customer_phone válido: {package.customer_phone}")
        
        # Verificar la consulta específica que se usa en el template
        print(f"\n🔍 Verificando consulta específica del template:")
        print(f"  - Filtro: is_active == True")
        print(f"  - Orden: desc(announced_at)")
        print(f"  - Límite: 10")
        
        # Probar la consulta exacta del dashboard
        dashboard_packages = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_active == True
        ).order_by(desc(PackageAnnouncement.announced_at)).limit(10).all()
        
        print(f"\n📋 Datos que se pasan al template:")
        for package in dashboard_packages:
            print(f"  - {package.tracking_code}: {package.customer_name} - {package.customer_phone}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard_data()
