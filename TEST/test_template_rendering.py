#!/usr/bin/env python3
"""
Script para probar el renderizado del template con datos reales
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
project_root = "/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code"
sys.path.insert(0, project_root)

from src.database.database import get_db
from src.models.announcement import PackageAnnouncement
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

def test_template_rendering():
    """Probar el renderizado del template con datos reales"""
    
    print("🔍 Probando renderizado del template...")
    print("=" * 60)
    
    try:
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Obtener datos como lo hace el dashboard
        recent_packages = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_active == True
        ).order_by(desc(PackageAnnouncement.announced_at)).limit(3).all()
        
        print(f"📊 Datos obtenidos del backend:")
        for i, package in enumerate(recent_packages):
            print(f"\n📦 Paquete {i+1}:")
            print(f"  - tracking_code: {package.tracking_code}")
            print(f"  - customer_name: {package.customer_name}")
            print(f"  - customer_phone: {package.customer_phone}")
            print(f"  - guide_number: {package.guide_number}")
            print(f"  - announced_at: {package.announced_at}")
            
            # Simular la lógica del template
            phone_display = package.customer_phone if package.customer_phone else 'Sin teléfono'
            print(f"  - phone_display (template logic): {phone_display}")
            
            # Verificar si el problema está en la lógica del template
            if package.customer_phone:
                if package.customer_phone == 'undefined':
                    print(f"  ❌ PROBLEMA: customer_phone es string 'undefined'")
                elif package.customer_phone == '':
                    print(f"  ❌ PROBLEMA: customer_phone es string vacío")
                elif package.customer_phone is None:
                    print(f"  ❌ PROBLEMA: customer_phone es None")
                else:
                    print(f"  ✅ customer_phone válido: {package.customer_phone}")
            else:
                print(f"  ⚠️ customer_phone es falsy: {package.customer_phone}")
        
        # Probar la lógica específica del template
        print(f"\n🎯 Probando lógica del template:")
        for package in recent_packages:
            # Esta es la lógica exacta del template
            template_phone = package.customer_phone if package.customer_phone else 'Sin teléfono'
            print(f"  - {package.tracking_code}: {template_phone}")
            
            # Verificar si hay algún problema con la evaluación
            print(f"    - package.customer_phone: {repr(package.customer_phone)}")
            print(f"    - bool(package.customer_phone): {bool(package.customer_phone)}")
            print(f"    - template_phone: {repr(template_phone)}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_template_rendering()
