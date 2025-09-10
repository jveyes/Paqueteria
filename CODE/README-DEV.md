# 🚀 Entorno de Desarrollo - PAQUETES EL CLUB v3.1

## 📋 Descripción

Este entorno de desarrollo permite trabajar con **hot reload** y **cambios instantáneos** sin necesidad de reconstruir contenedores.

## 🛠️ Características

- ✅ **Hot Reload**: Cambios instantáneos en código
- ✅ **Volúmenes Montados**: Código en el host, servicios en contenedores
- ✅ **Base de Datos Persistente**: Datos se mantienen entre reinicios
- ✅ **Scripts Automatizados**: Inicio/parada fácil
- ✅ **Separación de Responsabilidades**: Código vs Servicios

## 🚀 Inicio Rápido

### 1. Iniciar entorno de desarrollo
```bash
./start-dev.sh
```

### 2. Acceder a la aplicación
- **Aplicación**: http://localhost
- **API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

### 3. Ver logs
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

### 4. Parar entorno
```bash
./stop-dev.sh
```

## 📁 Estructura de Volúmenes

```
code/
├── src/           → Montado en /app/src
├── templates/     → Montado en /app/templates
├── static/        → Montado en /app/static
├── alembic/       → Montado en /app/alembic
└── logs/          → Montado en /app/logs
```

## 🔧 Comandos Útiles

### Reiniciar solo la aplicación
```bash
docker-compose -f docker-compose.dev.yml restart app
```

### Ver logs de un servicio específico
```bash
docker-compose -f docker-compose.dev.yml logs -f app
docker-compose -f docker-compose.dev.yml logs -f postgres
```

### Acceder al contenedor
```bash
docker-compose -f docker-compose.dev.yml exec app bash
```

### Limpiar todo (incluyendo datos)
```bash
docker-compose -f docker-compose.dev.yml down -v
```

## 🐛 Solución de Problemas

### El código no se actualiza
1. Verificar que los volúmenes estén montados:
   ```bash
   docker-compose -f docker-compose.dev.yml exec app ls -la /app/src
   ```

2. Reiniciar solo la aplicación:
   ```bash
   docker-compose -f docker-compose.dev.yml restart app
   ```

### Error de base de datos
1. Verificar que PostgreSQL esté ejecutándose:
   ```bash
   docker-compose -f docker-compose.dev.yml ps postgres
   ```

2. Ver logs de PostgreSQL:
   ```bash
   docker-compose -f docker-compose.dev.yml logs postgres
   ```

### Puerto ocupado
1. Verificar qué está usando el puerto:
   ```bash
   lsof -i :80
   lsof -i :8000
   ```

2. Cambiar puertos en `docker-compose.dev.yml` si es necesario

## 📊 Servicios Incluidos

- **app**: Aplicación FastAPI con hot reload
- **postgres**: Base de datos PostgreSQL
- **redis**: Cache y cola de tareas
- **nginx**: Proxy reverso
- **celery_worker**: Procesador de tareas en background

## 🔄 Flujo de Desarrollo

1. **Hacer cambios** en el código
2. **Guardar archivo**
3. **Ver cambios instantáneamente** (sin rebuild)
4. **Probar funcionalidad**
5. **Iterar rápidamente**

## 🚀 Ventajas vs Entorno Anterior

| Antes | Ahora |
|-------|-------|
| ❌ Rebuild 1-2 min | ✅ Cambios instantáneos |
| ❌ Frustración | ✅ Desarrollo ágil |
| ❌ Código en contenedor | ✅ Código en host |
| ❌ Sin hot reload | ✅ Hot reload automático |
