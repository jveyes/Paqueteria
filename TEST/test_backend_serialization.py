#!/usr/bin/env python3
"""
Script para investigar la serialización de datos en el backend
"""

import sys
import os
import json

# Agregar el directorio del proyecto al path
project_root = "/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code"
sys.path.insert(0, project_root)

from src.database.database import get_db
from src.models.announcement import PackageAnnouncement
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

def test_object_serialization():
    """Probar la serialización de objetos SQLAlchemy"""
    
    print("🔍 Probando serialización de objetos...")
    print("=" * 60)
    
    try:
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Obtener un paquete de prueba
        package = db.query(PackageAnnouncement).first()
        
        if not package:
            print("❌ No se encontraron paquetes en la base de datos")
            return
        
        print(f"📦 Paquete de prueba:")
        print(f"  - ID: {package.id}")
        print(f"  - customer_name: {package.customer_name}")
        print(f"  - customer_phone: {package.customer_phone}")
        print(f"  - guide_number: {package.guide_number}")
        print(f"  - tracking_code: {package.tracking_code}")
        
        # Probar diferentes formas de acceso a los atributos
        print(f"\n🔍 Probando acceso a atributos:")
        print(f"  - getattr(package, 'customer_phone'): {getattr(package, 'customer_phone', 'NOT_FOUND')}")
        print(f"  - hasattr(package, 'customer_phone'): {hasattr(package, 'customer_phone')}")
        print(f"  - package.__dict__.get('customer_phone'): {package.__dict__.get('customer_phone', 'NOT_FOUND')}")
        
        # Probar serialización a JSON
        print(f"\n🔍 Probando serialización a JSON:")
        try:
            # Intentar serializar directamente
            json_data = json.dumps(package.__dict__, default=str)
            print(f"  - JSON serialization: {json_data[:200]}...")
        except Exception as e:
            print(f"  - Error en serialización JSON: {e}")
        
        # Probar acceso a través de vars()
        print(f"\n🔍 Probando vars():")
        vars_dict = vars(package)
        print(f"  - vars(package).get('customer_phone'): {vars_dict.get('customer_phone', 'NOT_FOUND')}")
        
        # Probar acceso a través de dir()
        print(f"\n🔍 Atributos disponibles:")
        attrs = [attr for attr in dir(package) if not attr.startswith('_')]
        print(f"  - Atributos: {attrs}")
        
        # Verificar si customer_phone está en los atributos
        if 'customer_phone' in attrs:
            print(f"  ✅ customer_phone está en dir()")
        else:
            print(f"  ❌ customer_phone NO está en dir()")
        
        # Probar acceso directo al atributo
        print(f"\n🔍 Probando acceso directo:")
        try:
            phone_value = package.customer_phone
            print(f"  - package.customer_phone: {repr(phone_value)}")
            print(f"  - type: {type(phone_value)}")
            print(f"  - is None: {phone_value is None}")
            print(f"  - bool: {bool(phone_value)}")
        except Exception as e:
            print(f"  - Error accediendo a customer_phone: {e}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_template_context():
    """Probar cómo se pasan los datos al template"""
    
    print("\n🔍 Probando contexto del template...")
    print("=" * 60)
    
    try:
        # Simular la lógica del dashboard
        db = next(get_db())
        
        recent_packages = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_active == True
        ).order_by(desc(PackageAnnouncement.announced_at)).limit(3).all()
        
        print(f"📊 Datos que se pasan al template:")
        for i, package in enumerate(recent_packages):
            print(f"\n📦 Paquete {i+1}:")
            print(f"  - tracking_code: {package.tracking_code}")
            print(f"  - customer_name: {package.customer_name}")
            print(f"  - customer_phone: {package.customer_phone}")
            
            # Simular la evaluación del template
            template_phone = package.customer_phone if package.customer_phone else 'Sin teléfono'
            print(f"  - template_phone: {template_phone}")
            
            # Verificar si el problema está en la evaluación condicional
            if package.customer_phone:
                print(f"    ✅ La condición 'if package.customer_phone' es True")
            else:
                print(f"    ❌ La condición 'if package.customer_phone' es False")
                print(f"    - package.customer_phone es: {repr(package.customer_phone)}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando investigación de serialización")
    
    # Probar serialización de objetos
    test_object_serialization()
    
    # Probar contexto del template
    test_template_context()
    
    print("\n🏁 Investigación completada")
