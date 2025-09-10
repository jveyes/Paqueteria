# 🏠 PAQUETES EL CLUB v3.5 - Configuración para Localhost

## ✅ **CONFIGURACIÓN COMPLETADA**

El proyecto **PAQUETES EL CLUB v3.5** ha sido configurado exitosamente para funcionar únicamente en **localhost**. Todas las referencias a `guia.papyrus.com.co` han sido removidas.

---

## 🚀 **INICIO RÁPIDO**

### **1. Iniciar el Proyecto**
```bash
# Opción 1: Usar el script automatizado (Recomendado)
./start-localhost.sh

# Opción 2: Comandos manuales
docker-compose up -d
```

### **2. Verificar que Funciona**
```bash
# Health check
curl http://localhost/health

# Ver estado de servicios
docker-compose ps
```

### **3. Acceder a la Aplicación**
- 🌐 **Aplicación Principal**: http://localhost
- 📚 **API Documentation**: http://localhost/docs
- 📊 **Health Check**: http://localhost/health
- 📈 **Prometheus**: http://localhost:9090
- 📊 **Grafana**: http://localhost:3000 (admin/Grafana2025!Secure)

---

## 🏗️ **ARQUITECTURA LOCAL**

### **Servicios Configurados**
- **PostgreSQL**: Base de datos local (puerto 5432)
- **Redis**: Cache y message broker (puerto 6379)
- **FastAPI**: Aplicación principal (puerto 8000)
- **Nginx**: Proxy reverso (puerto 80)
- **Celery**: Tareas en background
- **Prometheus**: Monitoreo (puerto 9090)
- **Grafana**: Dashboards (puerto 3000)

### **Base de Datos Local**
- **Host**: postgres (dentro de Docker)
- **Puerto**: 5432
- **Base de datos**: paqueteria_db
- **Usuario**: paqueteria_user
- **Contraseña**: paqueteria_pass

---

## 📋 **COMANDOS ÚTILES**

### **Gestión de Servicios**
```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs app
docker-compose logs postgres
docker-compose logs redis
```

### **Base de Datos**
```bash
# Acceder a PostgreSQL
docker-compose exec postgres psql -U paqueteria_user -d paqueteria_db

# Ejecutar migraciones (si es necesario)
docker-compose exec app alembic upgrade head

# Crear migración nueva
docker-compose exec app alembic revision --autogenerate -m "Descripción"
```

### **Desarrollo**
```bash
# Acceder al contenedor de la aplicación
docker-compose exec app bash

# Reconstruir imagen
docker-compose build --no-cache app

# Ver logs en tiempo real
docker-compose logs -f app
```

---

## 🔧 **CONFIGURACIÓN TÉCNICA**

### **Variables de Entorno**
El proyecto está configurado con las siguientes variables principales:
- `DATABASE_URL`: postgresql://paqueteria_user:paqueteria_pass@postgres:5432/paqueteria_db
- `REDIS_URL`: redis://redis:6379/0
- `ENVIRONMENT`: development
- `DEBUG`: True

### **Puertos Expuestos**
- **80**: Nginx (aplicación principal)
- **5432**: PostgreSQL
- **9090**: Prometheus
- **3000**: Grafana

### **Volúmenes Persistentes**
- `postgres_data`: Datos de PostgreSQL
- `redis_data`: Datos de Redis
- `grafana_data`: Configuración de Grafana
- `prometheus_data`: Métricas de Prometheus

---

## 🧪 **TESTING**

### **Verificar Funcionalidad**
```bash
# Health check
curl http://localhost/health

# API endpoints
curl http://localhost/api/health
curl http://localhost/docs

# Verificar base de datos
docker-compose exec postgres pg_isready -U paqueteria_user -d paqueteria_db
```

### **Logs de Debugging**
```bash
# Ver todos los logs
docker-compose logs

# Logs específicos
docker-compose logs app | grep ERROR
docker-compose logs postgres | grep ERROR
```

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Problemas Comunes**

#### **1. Servicios no inician**
```bash
# Verificar logs
docker-compose logs

# Reconstruir imágenes
docker-compose build --no-cache

# Limpiar recursos
docker system prune -f
```

#### **2. Base de datos no conecta**
```bash
# Verificar PostgreSQL
docker-compose logs postgres

# Verificar red Docker
docker network ls
```

#### **3. Puerto 80 ocupado**
```bash
# Verificar qué usa el puerto 80
sudo netstat -tulpn | grep :80

# Detener otros servicios que usen el puerto 80
sudo systemctl stop apache2  # Si usa Apache
sudo systemctl stop nginx    # Si usa Nginx local
```

#### **4. Problemas de permisos**
```bash
# Verificar permisos de archivos
ls -la code/uploads/
ls -la code/logs/

# Corregir permisos si es necesario
sudo chown -R $USER:$USER code/uploads/
sudo chown -R $USER:$USER code/logs/
```

---

## 📊 **MONITOREO**

### **Métricas Disponibles**
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
  - Usuario: admin
  - Contraseña: Grafana2025!Secure

### **Health Checks**
- **Aplicación**: http://localhost/health
- **API**: http://localhost/api/health

---

## 🔄 **DESARROLLO**

### **Flujo de Trabajo**
1. **Hacer cambios** en el código
2. **Reconstruir** la imagen si es necesario: `docker-compose build app`
3. **Reiniciar** el servicio: `docker-compose restart app`
4. **Verificar** que funciona: `curl http://localhost/health`

### **Hot Reload**
Para desarrollo con hot reload, puedes modificar el docker-compose.yml para montar el código como volumen:
```yaml
volumes:
  - ./code/src:/app/src:ro
```

---

## 📝 **NOTAS IMPORTANTES**

### **✅ Cambios Realizados**
- ✅ Removidas todas las referencias a `guia.papyrus.com.co`
- ✅ Configurado PostgreSQL local
- ✅ Configurado Redis local
- ✅ Ajustado Nginx para localhost
- ✅ Configurado variables de entorno para desarrollo
- ✅ Creado script de inicio automatizado

### **🔒 Seguridad**
- Las contraseñas son para desarrollo local únicamente
- No usar estas credenciales en producción
- El modo DEBUG está habilitado para desarrollo

### **📁 Archivos Modificados**
- `docker-compose.yml`: Configuración para localhost
- `code/nginx/nginx.conf`: Nginx para localhost
- `code/src/config.py`: Configuración de base de datos local
- `code/init.sql`: Inicialización de PostgreSQL
- `start-localhost.sh`: Script de inicio automatizado

---

## 🎉 **¡LISTO PARA USAR!**

El proyecto **PAQUETES EL CLUB v3.5** está completamente configurado para funcionar en localhost. 

**Acceso principal**: http://localhost

**Comando de inicio**: `./start-localhost.sh`

---

*Configurado el 6 de septiembre de 2025*
