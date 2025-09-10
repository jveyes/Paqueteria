#!/usr/bin/env python3
"""
Script para monitorear logs en tiempo real y detectar errores
"""

import os
import time
import subprocess
from datetime import datetime

def monitor_logs():
    """Monitorear logs en tiempo real"""
    log_file = "server.log"
    
    if not os.path.exists(log_file):
        print(f"❌ Archivo de log {log_file} no encontrado")
        return
    
    print(f"🔍 Monitoreando {log_file} en tiempo real...")
    print("Presiona Ctrl+C para salir")
    print("-" * 50)
    
    try:
        # Usar tail -f para seguir el archivo en tiempo real
        process = subprocess.Popen(
            ['tail', '-f', log_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        while True:
            line = process.stdout.readline()
            if line:
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # Detectar errores
                if any(keyword in line.lower() for keyword in ['error', 'exception', 'traceback', 'failed']):
                    print(f"🚨 [{timestamp}] ERROR: {line.strip()}")
                elif 'warning' in line.lower():
                    print(f"⚠️  [{timestamp}] WARNING: {line.strip()}")
                else:
                    print(f"ℹ️  [{timestamp}] {line.strip()}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n👋 Monitoreo detenido")
        process.terminate()
    except Exception as e:
        print(f"❌ Error en monitoreo: {e}")

if __name__ == "__main__":
    monitor_logs()
