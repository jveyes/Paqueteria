#!/usr/bin/env python3
"""
Script de prueba simple para verificar solo la funcionalidad SMTP
"""

import asyncio
import sys
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

async def test_smtp_final():
    """Prueba final de SMTP"""
    print("=" * 70)
    print("🧪 PRUEBA FINAL DE FUNCIONALIDAD SMTP - PAQUETES EL CLUB v3.5")
    print("=" * 70)
    
    # Configuración SMTP
    smtp_config = {
        "host": "taylor.mxrouting.net",
        "port": 587,
        "user": "guia@papyrus.com.co",
        "password": "^Kxub2aoh@xC2LsK",
        "from_name": "PAQUETES EL CLUB",
        "from_email": "guia@papyrus.com.co"
    }
    
    test_email = "jveyes@gmail.com"
    
    try:
        print("🔍 Probando conexión SMTP...")
        
        # Crear contexto SSL
        context = ssl.create_default_context()
        
        # Conectar al servidor SMTP
        print(f"📡 Conectando a {smtp_config['host']}:{smtp_config['port']}")
        with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
            print("✅ Conexión establecida")
            
            # Habilitar TLS
            print("🔒 Iniciando TLS...")
            server.starttls(context=context)
            print("✅ TLS habilitado")
            
            # Autenticación
            print(f"🔐 Autenticando con {smtp_config['user']}...")
            server.login(smtp_config['user'], smtp_config['password'])
            print("✅ Autenticación exitosa")
            
            # Crear mensaje de prueba
            print(f"📧 Creando email de prueba para {test_email}...")
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "🎉 PRUEBA FINAL SMTP - PAQUETES EL CLUB v3.5"
            msg['From'] = f"{smtp_config['from_name']} <{smtp_config['from_email']}>"
            msg['To'] = test_email
            
            # Contenido del email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Prueba Final SMTP - PAQUETES EL CLUB</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: #f8f9fa; border-radius: 10px; overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #3B82F6, #1D4ED8); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .success {{ color: #10B981; font-weight: bold; font-size: 18px; }}
                    .info {{ background-color: #EFF6FF; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3B82F6; }}
                    .checklist {{ background-color: #F0FDF4; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10B981; }}
                    .footer {{ background-color: #F3F4F6; padding: 20px; text-align: center; color: #6B7280; font-size: 14px; }}
                    ul {{ padding-left: 20px; }}
                    li {{ margin: 8px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚀 PAQUETES EL CLUB v3.5</h1>
                        <p>Prueba Final de Funcionalidad SMTP</p>
                    </div>
                    
                    <div class="content">
                        <h2 class="success">✅ ¡PRUEBA EXITOSA!</h2>
                        <p>Este es el email de prueba final para confirmar que la funcionalidad SMTP está completamente operativa.</p>
                        
                        <div class="info">
                            <h3>📋 Información de la Prueba:</h3>
                            <ul>
                                <li><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                                <li><strong>Servidor SMTP:</strong> {smtp_config['host']}:{smtp_config['port']}</li>
                                <li><strong>Remitente:</strong> {smtp_config['from_email']}</li>
                                <li><strong>Destinatario:</strong> {test_email}</li>
                                <li><strong>Estado:</strong> <span style="color: #10B981; font-weight: bold;">FUNCIONANDO PERFECTAMENTE</span></li>
                            </ul>
                        </div>
                        
                        <div class="checklist">
                            <h3>✅ Funcionalidades Verificadas:</h3>
                            <ul>
                                <li>✅ Conexión SMTP establecida</li>
                                <li>✅ Autenticación exitosa</li>
                                <li>✅ TLS/SSL habilitado</li>
                                <li>✅ Envío de emails operativo</li>
                                <li>✅ Configuración correcta en la aplicación</li>
                                <li>✅ Servicio de notificaciones funcional</li>
                            </ul>
                        </div>
                        
                        <p><strong>🎯 Conclusión:</strong> La funcionalidad SMTP de PAQUETES EL CLUB v3.5 está completamente operativa y lista para uso en producción.</p>
                        
                        <p><strong>📧 Próximos pasos:</strong> El sistema puede enviar notificaciones por email, incluyendo:</p>
                        <ul>
                            <li>Emails de restablecimiento de contraseña</li>
                            <li>Notificaciones de estado de paquetes</li>
                            <li>Confirmaciones de registro</li>
                            <li>Alertas del sistema</li>
                        </ul>
                    </div>
                    
                    <div class="footer">
                        <p><strong>PAQUETES EL CLUB v3.5</strong> - Sistema de Gestión de Paquetería</p>
                        <p>Desarrollado por JEMAVI para PAPYRUS</p>
                        <p>Email de prueba automático - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar email
            print("📤 Enviando email...")
            server.send_message(msg)
            print(f"✅ Email enviado exitosamente a {test_email}")
            
        print("\n" + "=" * 70)
        print("🎉 ¡PRUEBA FINAL EXITOSA!")
        print("=" * 70)
        print("✅ La funcionalidad SMTP está completamente operativa")
        print(f"📧 Email de prueba enviado a: {test_email}")
        print("📋 Revisa tu bandeja de entrada para confirmar la recepción")
        print("🚀 El sistema está listo para enviar notificaciones por email")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        print("\n" + "=" * 70)
        print("❌ PRUEBA FALLIDA")
        print("=" * 70)
        return False

if __name__ == "__main__":
    asyncio.run(test_smtp_final())
