#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.5 - Test de Conexión
# ========================================

import os
import sys
import psycopg2
import redis
import requests
from urllib.parse import urlparse

def test_database_connection():
    """Probar conexión a PostgreSQL RDS"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL no configurado")
            return False
        
        # Parsear URL de conexión
        parsed = urlparse(database_url)
        
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"✅ Conexión a PostgreSQL exitosa: {version[0][:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return False

def test_redis_connection():
    """Probar conexión a Redis"""
    try:
        redis_url = os.getenv('REDIS_URL')
        if not redis_url:
            print("❌ REDIS_URL no configurado")
            return False
        
        r = redis.from_url(redis_url)
        r.ping()
        
        print("✅ Conexión a Redis exitosa")
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a Redis: {e}")
        return False

def test_smtp_connection():
    """Probar configuración SMTP"""
    try:
        smtp_host = os.getenv('SMTP_HOST')
        smtp_port = os.getenv('SMTP_PORT')
        smtp_user = os.getenv('SMTP_USER')
        
        if not all([smtp_host, smtp_port, smtp_user]):
            print("❌ Configuración SMTP incompleta")
            return False
        
        print(f"✅ Configuración SMTP: {smtp_user}@{smtp_host}:{smtp_port}")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración SMTP: {e}")
        return False

def test_liwa_config():
    """Probar configuración LIWA"""
    try:
        liwa_api_key = os.getenv('LIWA_API_KEY')
        liwa_account = os.getenv('LIWA_ACCOUNT')
        
        if not all([liwa_api_key, liwa_account]):
            print("❌ Configuración LIWA incompleta")
            return False
        
        print(f"✅ Configuración LIWA: {liwa_account}")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración LIWA: {e}")
        return False

def test_app_health():
    """Probar health check de la aplicación"""
    try:
        response = requests.get('http://localhost/health', timeout=10)
        if response.status_code == 200:
            print("✅ Health check de aplicación exitoso")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🔍 PAQUETES EL CLUB v3.5 - Test de Conexiones")
    print("=" * 50)
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    tests = [
        ("Base de Datos PostgreSQL", test_database_connection),
        ("Redis Cache", test_redis_connection),
        ("Configuración SMTP", test_smtp_connection),
        ("Configuración LIWA", test_liwa_config),
        ("Health Check App", test_app_health),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Probando {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} tests pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todas las conexiones funcionan correctamente!")
        return 0
    else:
        print("⚠️  Algunas conexiones fallaron. Revisar configuración.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
