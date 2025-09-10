#!/usr/bin/env python3
"""
Script para analizar el HTML generado y encontrar el problema
"""

import requests
import re

def analyze_dashboard_html():
    """Analizar el HTML del dashboard para encontrar el problema"""
    
    print("🔍 Analizando HTML del dashboard...")
    print("=" * 60)
    
    try:
        # Hacer petición al dashboard
        response = requests.get("http://localhost/dashboard", timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            print(f"📊 Estadísticas del HTML:")
            print(f"  - Longitud total: {len(html_content)} caracteres")
            print(f"  - Líneas totales: {len(html_content.split(chr(10)))}")
            
            # Buscar todas las ocurrencias de "undefined"
            undefined_matches = re.finditer(r'undefined', html_content)
            print(f"\n❌ Ocurrencias de 'undefined':")
            for i, match in enumerate(undefined_matches):
                start = max(0, match.start() - 50)
                end = min(len(html_content), match.end() + 50)
                context = html_content[start:end]
                print(f"  {i+1}. Contexto: ...{context}...")
            
            # Buscar patrones de teléfono
            phone_patterns = [
                r'customer_phone',
                r'Sin teléfono',
                r'3002596319',
                r'3008103849',
                r'3128432422',
                r'3024546729'
            ]
            
            print(f"\n🔍 Patrones encontrados:")
            for pattern in phone_patterns:
                matches = re.findall(pattern, html_content)
                print(f"  - '{pattern}': {len(matches)} ocurrencias")
                if matches:
                    print(f"    Ejemplos: {matches[:3]}")
            
            # Buscar líneas específicas del template
            lines = html_content.split('\n')
            print(f"\n🔍 Líneas relevantes del template:")
            for i, line in enumerate(lines):
                if 'customer_phone' in line or 'Sin teléfono' in line or 'undefined' in line:
                    print(f"  Línea {i+1}: {line.strip()}")
            
            # Buscar el patrón específico del template que modificamos
            template_pattern = r'{% if package\.customer_phone %}'
            if re.search(template_pattern, html_content):
                print(f"\n✅ Patrón del template encontrado: {template_pattern}")
            else:
                print(f"\n❌ Patrón del template NO encontrado: {template_pattern}")
            
            # Buscar el patrón antiguo
            old_pattern = r'package\.customer_phone if package\.customer_phone else'
            if re.search(old_pattern, html_content):
                print(f"\n⚠️ Patrón antiguo encontrado: {old_pattern}")
            else:
                print(f"\n✅ Patrón antiguo NO encontrado: {old_pattern}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def analyze_announcement_detail_html():
    """Analizar el HTML de la vista de detalles"""
    
    print("\n🔍 Analizando HTML de vista de detalles...")
    print("=" * 60)
    
    test_codes = ["DSVS", "N61P"]
    
    for code in test_codes:
        print(f"\n📦 Analizando código: {code}")
        
        try:
            response = requests.get(f"http://localhost/announcements/guide/{code}", timeout=10)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Buscar patrones específicos
                patterns = ['customer_phone', 'Sin teléfono', 'undefined', '3002596319']
                for pattern in patterns:
                    matches = re.findall(pattern, html_content)
                    print(f"  - '{pattern}': {len(matches)} ocurrencias")
                
                # Buscar líneas relevantes
                lines = html_content.split('\n')
                for i, line in enumerate(lines):
                    if 'customer_phone' in line or 'Sin teléfono' in line or 'undefined' in line:
                        print(f"    Línea {i+1}: {line.strip()}")
                        
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando análisis del HTML")
    
    # Analizar dashboard
    analyze_dashboard_html()
    
    # Analizar vista de detalles
    analyze_announcement_detail_html()
    
    print("\n🏁 Análisis completado")
