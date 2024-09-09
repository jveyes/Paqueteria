# 🚀 PAQUETES EL CLUB v3.5

Sistema de gestión de paquetería optimizado para producción con Docker, SSL/HTTPS y monitoreo completo.

## 📋 Características

- ✅ **FastAPI** con Python 3.11
- ✅ **PostgreSQL** (AWS RDS)
- ✅ **Redis** para cache y tareas en background
- ✅ **Nginx** con SSL/HTTPS
- ✅ **Celery** para tareas asíncronas
- ✅ **Prometheus + Grafana** para monitoreo
- ✅ **Docker Compose** para orquestación
- ✅ **Puerto 80** para producción

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx (80/443)│    │   FastAPI App   │    │   PostgreSQL    │
│   SSL/HTTPS     │◄──►│   (Puerto 8000) │◄──►│   (AWS RDS)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Redis Cache   │    │  Celery Worker  │    │   Prometheus    │
│   (Puerto 6379) │    │   (Background)  │    │   + Grafana     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Inicio Rápido

### 1. Configurar Variables de Entorno
```bash
# El archivo .env ya está configurado con las credenciales
# Verificar que las credenciales de RDS estén correctas
```

### 2. Generar Certificados SSL (Desarrollo)
```bash
cd code/nginx/ssl
./generate-ssl.sh
```

### 3. Desplegar Servicios
```bash
# Usar el script de despliegue automatizado
./SCRIPTS/deploy-production.sh

# O manualmente
docker-compose up -d
```

### 4. Verificar Despliegue
```bash
# Verificar estado de servicios
docker-compose ps

# Ver logs
docker-compose logs -f

# Health check
curl http://localhost/health
```

## 🌐 URLs de Acceso

- **Aplicación**: http://localhost
- **API Docs**: http://localhost/docs
- **Health Check**: http://localhost/health
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/Grafana2025!Secure)

## 📁 Estructura del Proyecto

```
Paqueteria v3.5/
├── code/                    # Código principal
│   ├── src/                # Código fuente Python
│   ├── templates/          # Plantillas HTML
│   ├── static/             # Archivos estáticos
│   ├── alembic/            # Migraciones de BD
│   ├── nginx/              # Configuración nginx
│   └── Dockerfile          # Imagen Docker optimizada
├── docker-compose.yml      # Orquestación de servicios
├── .env                    # Variables de entorno
├── TEST/                   # Archivos de testing
├── SCRIPTS/                # Scripts de utilidad
├── DOCS/                   # Documentación
└── BACKUPS/                # Respaldos
```

## 🔧 Comandos Útiles

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Acceder a contenedor
docker-compose exec app bash

# Ver logs de un servicio específico
docker-compose logs app
docker-compose logs nginx
docker-compose logs redis
```

## 🔒 Configuración SSL

### Para Desarrollo
- Certificados autofirmados incluidos
- Ejecutar `code/nginx/ssl/generate-ssl.sh`

### Para Producción
- Reemplazar certificados en `code/nginx/ssl/`
- Usar Let's Encrypt o certificados de CA
- Actualizar configuración en `code/nginx/nginx.conf`

## 📊 Monitoreo

### Prometheus
- Métricas de aplicación: http://localhost:9090
- Configuración: `code/nginx/prometheus.yml`

### Grafana
- Dashboards: http://localhost:3000
- Usuario: admin
- Contraseña: Grafana2025!Secure

## 🗄️ Base de Datos

- **Tipo**: PostgreSQL (AWS RDS)
- **Host**: ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com
- **Puerto**: 5432
- **Base de datos**: paqueteria
- **Migraciones**: Alembic incluido

## 📧 Notificaciones

### Email
- **SMTP**: taylor.mxrouting.net
- **Puerto**: 587
- **Usuario**: guia@papyrus.com.co

### SMS
- **Proveedor**: LIWA.co
- **API Key**: Configurada en .env

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error de conexión a RDS**
   ```bash
   # Verificar credenciales en .env
   # Verificar conectividad de red
   ```

2. **Error de SSL**
   ```bash
   # Regenerar certificados
   cd code/nginx/ssl && ./generate-ssl.sh
   ```

3. **Servicios no inician**
   ```bash
   # Ver logs
   docker-compose logs
   
   # Verificar puertos ocupados
   netstat -tulpn | grep :80
   ```

### Logs Importantes
```bash
# Logs de aplicación
docker-compose logs app

# Logs de nginx
docker-compose logs nginx

# Logs de Redis
docker-compose logs redis
```

## 🔄 Migración desde v3.1

1. **Datos**: No se requieren scripts de migración
2. **Configuración**: Usar mismo archivo .env
3. **Base de datos**: Misma instancia RDS
4. **Archivos**: Copiar uploads/ si es necesario

## 📞 Soporte

- **Logs**: `docker-compose logs -f`
- **Estado**: `docker-compose ps`
- **Health**: http://localhost/health
- **Documentación**: Ver carpeta DOCS/

---

**Versión**: 3.5.0  
**Fecha**: Enero 2025  
**Autor**: Equipo PAPYRUS  
**Estado**: Listo para Producción
