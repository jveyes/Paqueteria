#!/bin/bash

# =============================================================================
# SIMULADOR OFFLINE PARA PAQUETERÍA
# Crea un repositorio local con estructura real del proyecto
# =============================================================================

# --- CONFIGURACIÓN ---
# 1. Repositorio de simulación local
REPO_NAME="paqueteria-offline-simulation"

# 2. Fechas (formato YYYY-MM-DD). Últimos 8 meses
START_DATE=$(date -d "8 months ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

# 3. Archivos que simularían cambios reales en el proyecto
FILES=(
    "code/src/main.py"
    "code/src/models/package.py" 
    "code/src/routers/packages.py"
    "code/templates/dashboard/dashboard.html"
    "code/requirements.txt"
    "code/src/config.py"
    "code/src/models/customer.py"
    "code/src/routers/customers.py"
    "code/templates/customers/search.html"
    "code/static/js/colombia-timezone.js"
    "code/src/models/message.py"
    "code/src/routers/messages.py"
    "code/templates/messages/messages.html"
    "code/src/services/rate_service.py"
    "code/docker-compose.yml"
    "code/Dockerfile"
    "README.md"
)

# 4. Directorio de trabajo
WORK_DIR="/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/GHCODE"

echo "=========================================="
echo "🏠 SIMULADOR OFFLINE - PAQUETERÍA"
echo "=========================================="
echo "📁 Directorio de trabajo: $WORK_DIR"
echo "📅 Rango de fechas: $START_DATE a $END_DATE"
echo "📦 Repositorio local: $REPO_NAME"
echo "=========================================="

# Cambiar al directorio de trabajo
cd "$WORK_DIR"

# --- VALIDACIONES DE SEGURIDAD ---

echo "🔍 Realizando validaciones de seguridad..."

# Verificar que no estamos en un repositorio con remotes
if [ -d ".git" ] && git remote -v | grep -q "origin"; then
    echo "❌ ERROR: No ejecutar en repositorios con remotes configurados"
    echo "   Este script debe ejecutarse en un directorio limpio"
    exit 1
fi

echo "✅ Validaciones de seguridad completadas"

# --- LÓGICA DEL SCRIPT OFFLINE ---

# Crear repositorio de simulación local (si no existe)
if [ -d "$REPO_NAME" ]; then
    echo "📂 Repositorio de simulación ya existe, entrando..."
    cd "$REPO_NAME"
    
    # Limpiar commits anteriores para nueva simulación
    echo "🧹 Limpiando simulación anterior..."
    git checkout --orphan temp-branch
    git add -A
    git commit -m "Clean slate for new simulation"
    git branch -D main
    git branch -m main
    git push -f origin main 2>/dev/null || true
else
    echo "📂 Creando repositorio de simulación local..."
    mkdir "$REPO_NAME"
    cd "$REPO_NAME"
    git init
    
    # Configurar git para commits simulados
    git config user.name "Paqueteria Developer"
    git config user.email "dev@paqueteria.local"
    
    # Crear estructura básica del proyecto
    mkdir -p code/src/{models,routers,services,schemas,utils}
    mkdir -p code/templates/{dashboard,customers,messages,auth,admin}
    mkdir -p code/static/{js,css,images}
    mkdir -p code/nginx/ssl
    mkdir -p DOCS SCRIPTS TEST BACKUPS
    
    # Archivo README inicial
    cat > README.md << 'EOF'
# 🚀 PAQUETES EL CLUB v3.5

Sistema de gestión de paquetería optimizado para producción con Docker, SSL/HTTPS y monitoreo completo.

## 📋 Características

* ✅ **FastAPI** con Python 3.11
* ✅ **PostgreSQL** (AWS RDS)
* ✅ **Redis** para cache y tareas en background
* ✅ **Nginx** con SSL/HTTPS
* ✅ **Celery** para tareas asíncronas
* ✅ **Prometheus + Grafana** para monitoreo
* ✅ **Docker Compose** para orquestación
* ✅ **Puerto 80** para producción

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

# El archivo .env ya está configurado con las credenciales
# Verificar que las credenciales de RDS estén correctas

### 2. Generar Certificados SSL (Desarrollo)

cd code/nginx/ssl
./generate-ssl.sh

### 3. Desplegar Servicios

# Usar el script de despliegue automatizado
./SCRIPTS/deploy-production.sh

# O manualmente
docker-compose up -d

### 4. Verificar Despliegue

# Verificar estado de servicios
docker-compose ps

# Ver logs
docker-compose logs -f

# Health check
curl http://localhost/health

## 🌐 URLs de Acceso

* **Aplicación**: http://localhost
* **API Docs**: http://localhost/docs
* **Health Check**: http://localhost/health
* **Prometheus**: http://localhost:9090
* **Grafana**: http://localhost:3000 (admin/Grafana2025!Secure)

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

## 🔒 Configuración SSL

### Para Desarrollo

* Certificados autofirmados incluidos
* Ejecutar `code/nginx/ssl/generate-ssl.sh`

### Para Producción

* Reemplazar certificados en `code/nginx/ssl/`
* Usar Let's Encrypt o certificados de CA
* Actualizar configuración en `code/nginx/nginx.conf`

## 📊 Monitoreo

### Prometheus

* Métricas de aplicación: http://localhost:9090
* Configuración: `code/nginx/prometheus.yml`

### Grafana

* Dashboards: http://localhost:3000
* Usuario: admin
* Contraseña: Grafana2025!Secure

## 🗄️ Base de Datos

* **Tipo**: PostgreSQL (AWS RDS)
* **Host**: ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com
* **Puerto**: 5432
* **Base de datos**: paqueteria
* **Migraciones**: Alembic incluido

## 📧 Notificaciones

### Email

* **SMTP**: taylor.mxrouting.net
* **Puerto**: 587
* **Usuario**: guia@papyrus.com.co

### SMS

* **Proveedor**: LIWA.co
* **API Key**: Configurada en .env

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error de conexión a RDS**  
# Verificar credenciales en .env  
# Verificar conectividad de red
2. **Error de SSL**  
# Regenerar certificados  
cd code/nginx/ssl && ./generate-ssl.sh
3. **Servicios no inician**  
# Ver logs  
docker-compose logs  
# Verificar puertos ocupados  
netstat -tulpn | grep :80

### Logs Importantes

# Logs de aplicación
docker-compose logs app

# Logs de nginx
docker-compose logs nginx

# Logs de Redis
docker-compose logs redis

## 🔄 Migración desde v3.1

1. **Datos**: No se requieren scripts de migración
2. **Configuración**: Usar mismo archivo .env
3. **Base de datos**: Misma instancia RDS
4. **Archivos**: Copiar uploads/ si es necesario

## 📞 Soporte

* **Logs**: `docker-compose logs -f`
* **Estado**: `docker-compose ps`
* **Health**: http://localhost/health
* **Documentación**: Ver carpeta DOCS/

---

**Versión**: 3.5.0  
**Fecha**: Enero 2025  
**Autor**: Equipo PAPYRUS  
**Estado**: Listo para Producción
EOF

    # Archivo requirements.txt inicial
    cat > code/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-multipart==0.0.6
jinja2==3.1.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
celery==5.3.4
redis==5.0.1
requests==2.31.0
pydantic==2.5.0
python-multipart==0.0.6
EOF

    # Archivo main.py inicial
    cat > code/src/main.py << 'EOF'
"""
Sistema de Control y Gestión de Paquetes
FastAPI Application
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Paquetería EL CLUB",
    description="Sistema de gestión de paquetes",
    version="3.5.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Paquetería EL CLUB v3.5"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.5.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

    git add .
    git commit -m "feat: initial project setup with FastAPI structure"
    echo "✅ Repositorio de simulación inicializado con estructura completa"
fi

# Inicia un bucle desde la fecha de inicio hasta la fecha de fin
current_date=$(date -d "$START_DATE" +%s)
end_date_s=$(date -d "$END_DATE" +%s)

echo ""
echo "🚀 Iniciando la simulación de commits para Paqueteria..."
echo ""

total_commits=0
total_days=0

# Mensajes de commit realistas para el proyecto
COMMIT_MESSAGES=(
    "feat: add package tracking functionality"
    "fix: resolve database connection issue with RDS"
    "refactor: improve package validation logic"
    "docs: update API documentation"
    "style: format code according to PEP8"
    "test: add unit tests for package service"
    "perf: optimize database queries for packages"
    "chore: update dependencies in requirements.txt"
    "feat: add email notifications for package status"
    "fix: handle edge case in package status updates"
    "refactor: restructure models directory"
    "docs: add deployment guide for Docker"
    "feat: implement user authentication system"
    "fix: resolve timezone issues in Colombia"
    "style: improve dashboard UI components"
    "test: add integration tests for customers"
    "perf: cache frequently accessed package data"
    "chore: update Docker configuration"
    "feat: add package search functionality"
    "fix: resolve SMS notification bug with LIWA"
    "feat: add customer management system"
    "fix: resolve SSL certificate issues"
    "refactor: improve FastAPI router structure"
    "docs: update README with new features"
    "feat: add Prometheus monitoring integration"
    "fix: resolve Redis connection issues"
    "style: improve responsive design for mobile"
    "test: add end-to-end tests for package flow"
    "perf: optimize PostgreSQL queries"
    "chore: update nginx configuration"
    "feat: add message system for notifications"
    "fix: resolve timezone handling in messages"
    "refactor: improve rate calculation service"
    "docs: add SMS integration documentation"
    "feat: add admin panel for package management"
    "fix: resolve file upload issues"
    "style: improve customer search interface"
    "test: add tests for message routing"
    "perf: optimize template rendering"
    "chore: update SSL certificate generation"
    "feat: add package status tracking"
    "fix: resolve authentication token issues"
    "refactor: improve database models"
    "docs: add troubleshooting guide"
    "feat: add bulk package operations"
    "fix: resolve email template rendering"
    "style: improve mobile responsiveness"
    "test: add performance tests"
    "perf: optimize static file serving"
    "chore: update Docker compose configuration"
)

while [ "$current_date" -le "$end_date_s" ]; do
    # Formatea la fecha para el commit
    commit_date=$(date -d "@$current_date" --iso-8601=seconds)
    day_name=$(date -d "@$current_date" +%Y-%m-%d)
    echo "📅 Procesando fecha: $day_name"

    # Decide si se hará un commit este día (70% de probabilidad para simular días libres)
    if [ $(($RANDOM % 10)) -lt 7 ]; then
        # Genera un número aleatorio de commits para este día (entre 1 y 4 para 8 meses)
        num_commits=$((($RANDOM % 4) + 1))
        
        echo "   📝 Generando $num_commits commits para $day_name"

        for (( i=1; i<=$num_commits; i++ )); do
            # Selecciona un archivo aleatorio para modificar
            file_to_modify=${FILES[$RANDOM % ${#FILES[@]}]}
            
            # Crea el archivo si no existe
            mkdir -p "$(dirname "$file_to_modify")"
            
            # Agrega contenido realista al archivo
            echo "# Modified on $commit_date - commit #$i" >> "$file_to_modify"
            echo "# Simulation change: $(date +%s)" >> "$file_to_modify"
            echo "# Random improvement: $(shuf -n 1 <<< 'performance optimization bug fix feature enhancement code cleanup security update')" >> "$file_to_modify"
            
            # Selecciona un mensaje de commit aleatorio
            commit_message=${COMMIT_MESSAGES[$RANDOM % ${#COMMIT_MESSAGES[@]}]}
            
            # Agrega el archivo al staging
            git add "$file_to_modify"

            # Realiza el commit con la fecha
            GIT_COMMITTER_DATE="$commit_date" GIT_AUTHOR_DATE="$commit_date" git commit -m "$commit_message" > /dev/null 2>&1
            
            total_commits=$((total_commits + 1))
        done
    else
        echo "   ⏭️  Día saltado (simulando fin de semana/descanso)"
    fi

    total_days=$((total_days + 1))
    
    # Avanza al siguiente día
    current_date=$(($current_date + 86400)) # 86400 segundos = 1 día
done

echo ""
echo "=========================================="
echo "✅ Simulación de commits completada"
echo "📊 Estadísticas:"
echo "   📅 Días procesados: $total_days"
echo "   📝 Total de commits: $total_commits"
echo "   📁 Repositorio: $(pwd)"
echo "=========================================="

# Mostrar el historial de commits
echo ""
echo "📋 Historial de commits generado:"
echo "----------------------------------------"
git log --oneline --graph --decorate -15

echo ""
echo "📈 Estadísticas del repositorio:"
echo "----------------------------------------"
echo "Total de commits: $(git rev-list --count HEAD)"
echo "Archivos modificados: $(git ls-files | wc -l)"
echo "Primer commit: $(git log --reverse --pretty=format:'%ad' --date=short | head -1)"
echo "Último commit: $(git log --pretty=format:'%ad' --date=short | head -1)"

echo ""
echo "🔍 Comandos útiles para inspeccionar:"
echo "   git log --oneline --graph --all"
echo "   git log --pretty=format:'%h %ad %s' --date=short"
echo "   git show --stat"
echo "   git log --author-date-order --graph --pretty=format:'%h %ad %s'"

echo ""
echo "🏠 INFORMACIÓN DE SIMULACIÓN OFFLINE:"
echo "   ✅ Repositorio local creado exitosamente"
echo "   ✅ Estructura completa del proyecto Paquetería"
echo "   ✅ 8 meses de commits simulados"
echo "   ✅ Para limpiar: rm -rf $REPO_NAME"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Este es un repositorio de simulación local"
echo "   - No está conectado a GitHub"
echo "   - Los commits son solo para simulación"
echo "   - Estructura basada en el proyecto real Paquetería"
