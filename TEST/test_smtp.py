#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad SMTP
"""

import asyncio
import sys
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append('/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/code')

# Configuración SMTP desde el .env
SMTP_CONFIG = {
    "host": "taylor.mxrouting.net",
    "port": 587,
    "user": "guia@papyrus.com.co",
    "password": "^Kxub2aoh@xC2LsK",
    "from_name": "PAQUETES EL CLUB",
    "from_email": "guia@papyrus.com.co"
}

async def test_smtp_connection():
    """Probar conexión SMTP básica"""
    print("🔍 Probando conexión SMTP...")
    
    try:
        # Crear contexto SSL
        context = ssl.create_default_context()
        
        # Conectar al servidor SMTP
        print(f"📡 Conectando a {SMTP_CONFIG['host']}:{SMTP_CONFIG['port']}")
        with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as server:
            print("✅ Conexión establecida")
            
            # Habilitar TLS
            print("🔒 Iniciando TLS...")
            server.starttls(context=context)
            print("✅ TLS habilitado")
            
            # Autenticación
            print(f"🔐 Autenticando con {SMTP_CONFIG['user']}...")
            server.login(SMTP_CONFIG['user'], SMTP_CONFIG['password'])
            print("✅ Autenticación exitosa")
            
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
        return False
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ Servidor desconectado: {e}")
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

async def test_send_email(to_email: str):
    """Probar envío de email"""
    print(f"\n📧 Probando envío de email a {to_email}...")
    
    try:
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🧪 Prueba SMTP - PAQUETES EL CLUB v3.5"
        msg['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        msg['To'] = to_email
        
        # Contenido del email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Prueba SMTP - PAQUETES EL CLUB</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #3B82F6; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background-color: #f8f9fa; padding: 20px; border-radius: 0 0 8px 8px; }}
                .success {{ color: #10B981; font-weight: bold; }}
                .info {{ background-color: #EFF6FF; padding: 15px; border-radius: 8px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 PAQUETES EL CLUB v3.5</h1>
                    <p>Prueba de Funcionalidad SMTP</p>
                </div>
                <div class="content">
                    <h2 class="success">✅ ¡Email enviado exitosamente!</h2>
                    <p>Este es un email de prueba para verificar que la funcionalidad SMTP está funcionando correctamente.</p>
                    
                    <div class="info">
                        <h3>📋 Información de la Prueba:</h3>
                        <ul>
                            <li><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                            <li><strong>Servidor SMTP:</strong> {SMTP_CONFIG['host']}:{SMTP_CONFIG['port']}</li>
                            <li><strong>Remitente:</strong> {SMTP_CONFIG['from_email']}</li>
                            <li><strong>Destinatario:</strong> {to_email}</li>
                            <li><strong>Estado:</strong> <span class="success">FUNCIONANDO</span></li>
                        </ul>
                    </div>
                    
                    <p>Si recibes este email, significa que:</p>
                    <ul>
                        <li>✅ La conexión SMTP está funcionando</li>
                        <li>✅ La autenticación es correcta</li>
                        <li>✅ El envío de emails está operativo</li>
                        <li>✅ El sistema de notificaciones puede funcionar</li>
                    </ul>
                    
                    <hr>
                    <p><small>Este es un email automático de prueba del sistema PAQUETES EL CLUB v3.5</small></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Agregar contenido HTML
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Configurar contexto SSL
        context = ssl.create_default_context()
        
        # Enviar email
        with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as server:
            server.starttls(context=context)
            server.login(SMTP_CONFIG['user'], SMTP_CONFIG['password'])
            server.send_message(msg)
            
        print(f"✅ Email enviado exitosamente a {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

async def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA DE FUNCIONALIDAD SMTP - PAQUETES EL CLUB v3.5")
    print("=" * 60)
    
    # Probar conexión
    connection_ok = await test_smtp_connection()
    
    if connection_ok:
        # Probar envío de email
        test_email = "jveyes@gmail.com"
        email_ok = await test_send_email(test_email)
        
        if email_ok:
            print("\n" + "=" * 60)
            print("🎉 ¡PRUEBA EXITOSA!")
            print("=" * 60)
            print("✅ La funcionalidad SMTP está funcionando correctamente")
            print(f"📧 Email de prueba enviado a: {test_email}")
            print("📋 Revisa tu bandeja de entrada (y spam) para confirmar la recepción")
        else:
            print("\n" + "=" * 60)
            print("❌ PRUEBA FALLIDA")
            print("=" * 60)
            print("❌ Error en el envío del email")
    else:
        print("\n" + "=" * 60)
        print("❌ PRUEBA FALLIDA")
        print("=" * 60)
        print("❌ Error en la conexión SMTP")

if __name__ == "__main__":
    asyncio.run(main())
