# ========================================
# PAQUETES EL CLUB v3.1 - Configuración Centralizada
# ========================================

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración centralizada de la aplicación"""
    
    # Configuración de la Aplicación
    app_name: str = "PAQUETES EL CLUB"
    app_version: str = "3.1.0"
    debug: bool = True
    environment: str = "development"
    
    # Base de Datos - Configuración por defecto (AWS RDS)
    database_url: str = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
    postgres_password: str = "a?HC!2.*1#?[==:|289qAI=)#V4kDzl$"
    postgres_user: str = "jveyes"
    postgres_db: str = "paqueteria"
    postgres_host: str = "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com"
    postgres_port: int = 5432
    
    # Configuración RDS - No necesitamos override para desarrollo
    
    # Cache Redis Local
    redis_url: str = "redis://redis:6379/0"
    redis_password: str = "Redis2025!Secure"
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Seguridad
    secret_key: str = "paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración SMTP
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_name: str = "PAQUETERIA EL CLUB"
    smtp_from_email: str = ""
    
    # Configuración SMS (LIWA.co) - SOLO SMS
    liwa_api_key: str = "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa"
    liwa_account: str = "00486396309"
    liwa_password: str = "6fEuRnd*$$#NfFAS"
    liwa_auth_url: str = "https://api.liwa.co/v2/auth/login"
    liwa_from_name: str = "PAQUETES EL CLUB"
    
    # NOTA: WhatsApp no está habilitado en esta versión
    # whatsapp_enabled: bool = False
    
    # Configuración de Tarifas
    base_storage_rate: int = 1000
    base_delivery_rate: int = 1500
    normal_package_multiplier: int = 1500
    extra_dimension_package_multiplier: int = 2000
    currency: str = "COP"
    
    # Configuración de Archivos
    upload_dir: str = "./uploads"
    max_file_size: int = 5242880  # 5MB
    allowed_extensions: str = "jpg,jpeg,png,gif,webp"
    
    # Configuración de la Empresa
    company_name: str = "PAQUETES EL CLUB"
    company_address: str = "Cra. 91 #54-120, Local 12"
    company_phone: str = "3334004007"
    company_email: str = "guia@papyrus.com.co"
    
    # Configuración de Monitoreo
    grafana_password: str = "Grafana2025!Secure"
    prometheus_port: int = 9090
    grafana_port: int = 3000
    
    # Configuración de Logs
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de autenticación
    secret_key: str = "paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración de PWA
    pwa_name: str = "PAQUETES EL CLUB"
    pwa_short_name: str = "Paquetes"
    pwa_description: str = "Sistema de gestión de paquetería"
    pwa_theme_color: str = "#3B82F6"
    pwa_background_color: str = "#FFFFFF"
    
    class Config:
        case_sensitive = False
        extra = "ignore"  # Ignorar variables extra

# Instancia global de configuración
try:
    settings = Settings()
except Exception as e:
    print(f"Error cargando configuración: {e}")
    # Usar configuración simple como fallback
    from .config_simple import settings
# Commit 4 - 2024-01-04
# Change: 1757423578
# Commit 7 - 2024-01-07
# Change: 1757423579
# Commit 9 - 2024-01-09
# Change: 1757423579
# Commit 25 - 2024-01-23
# Change: 1757423580
# Commit 33 - 2024-01-31
# Change: 1757423580
# Commit 41 - 2024-02-07
# Change: 1757423581
# Commit 51 - 2024-02-16
# Change: 1757423581
# Commit 74 - 2024-03-08
# Change: 1757423583
# Commit 75 - 2024-03-09
# Change: 1757423583
# Commit 81 - 2024-03-15
# Change: 1757423583
# Commit 89 - 2024-03-22
# Change: 1757423583
# Commit 103 - 2024-04-04
# Change: 1757423584
# Commit 109 - 2024-04-09
# Change: 1757423584
# Commit 114 - 2024-04-14
# Change: 1757423585
# Commit 125 - 2024-04-24
# Change: 1757423585
# Commit 129 - 2024-04-28
# Change: 1757423585
# Commit 136 - 2024-05-04
# Change: 1757423586
# Commit 152 - 2024-05-19
# Change: 1757423586
# Commit 161 - 2024-05-27
# Change: 1757423587
# Commit 164 - 2024-05-30
# Change: 1757423587
# Commit 174 - 2024-06-08
# Change: 1757423588
# Commit 187 - 2024-06-20
# Change: 1757423588
# Commit 193 - 2024-06-25
# Change: 1757423589
# Commit 194 - 2024-06-26
# Change: 1757423589
# Commit 204 - 2024-07-06
# Change: 1757423589
# Commit 207 - 2024-07-08
# Change: 1757423589
# Commit 220 - 2024-07-20
# Change: 1757423590
# Commit 223 - 2024-07-23
# Change: 1757423590
# Commit 224 - 2024-07-24
# Change: 1757423590
# Commit 235 - 2024-08-03
# Change: 1757423591
# Commit 244 - 2024-08-11
# Change: 1757423591
# Commit 253 - 2024-08-20
# Change: 1757423592
# Commit 254 - 2024-08-20
# Change: 1757423592
# Commit 267 - 2024-09-01
# Change: 1757423592
# Commit 273 - 2024-09-07
# Change: 1757423592
# Commit 277 - 2024-09-11
# Change: 1757423593
# Commit 281 - 2024-09-14
# Change: 1757423593
# Commit 283 - 2024-09-16
# Change: 1757423593
# Commit 289 - 2024-09-22
# Change: 1757423593
# Commit 305 - 2024-10-06
# Change: 1757423594
# Commit 307 - 2024-10-08
# Change: 1757423594
# Commit 315 - 2024-10-15
# Change: 1757423594
# Commit 321 - 2024-10-21
# Change: 1757423595
# Commit 336 - 2024-11-04
# Change: 1757423595
# Commit 339 - 2024-11-06
# Change: 1757423596
# Commit 340 - 2024-11-07
# Change: 1757423596
# Commit 343 - 2024-11-10
# Change: 1757423596
# Commit 370 - 2024-12-05
# Change: 1757423597
# Commit 375 - 2024-12-09
# Change: 1757423597
# Commit 389 - 2024-12-22
# Change: 1757423598
