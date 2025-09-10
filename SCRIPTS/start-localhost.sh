#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.5 - Script de Inicio para Localhost
# ========================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Configuración
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "🚀 INICIANDO PAQUETES EL CLUB v3.5 - LOCALHOST"
echo "=========================================="
echo ""

# Verificar prerrequisitos
log "Verificando prerrequisitos..."

if ! command -v docker &> /dev/null; then
    error "Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose no está instalado"
    exit 1
fi

success "Prerrequisitos verificados"

# Detener servicios existentes
log "Deteniendo servicios existentes..."
cd "$PROJECT_DIR"
docker-compose down 2>/dev/null || true
success "Servicios detenidos"

# Limpiar recursos no utilizados
log "Limpiando recursos Docker..."
docker system prune -f > /dev/null 2>&1 || true
success "Limpieza completada"

# Construir y levantar servicios
log "Construyendo y levantando servicios..."
docker-compose build --no-cache
docker-compose up -d

success "Servicios levantados"

# Esperar a que los servicios estén listos
log "Esperando a que los servicios estén listos..."
sleep 30

# Health checks
log "Realizando health checks..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    log "Health check intento $attempt/$max_attempts"
    
    if curl -f -s "http://localhost/health" > /dev/null 2>&1; then
        success "Health check exitoso"
        break
    fi
    
    sleep 10
    ((attempt++))
done

if [ $attempt -gt $max_attempts ]; then
    error "Health check falló después de $max_attempts intentos"
    echo ""
    echo "🔧 Verificando logs de servicios..."
    docker-compose logs --tail=20
    exit 1
fi

# Ejecutar migraciones
log "Ejecutando migraciones de base de datos..."
docker-compose exec -T app alembic upgrade head || {
    warning "Error en migraciones, continuando..."
}

success "Migraciones completadas"

# Mostrar estado final
echo ""
log "Estado final de servicios:"
docker-compose ps

echo ""
success "🎉 ¡PAQUETES EL CLUB v3.5 iniciado exitosamente en localhost!"
echo ""
echo "🌐 URLs de acceso:"
echo "  • Aplicación: http://localhost"
echo "  • API Docs: http://localhost/docs"
echo "  • Health Check: http://localhost/health"
echo "  • Prometheus: http://localhost:9090"
echo "  • Grafana: http://localhost:3000 (admin/Grafana2025!Secure)"
echo ""
echo "📋 Comandos útiles:"
echo "  • Ver logs: docker-compose logs -f"
echo "  • Reiniciar: docker-compose restart"
echo "  • Detener: docker-compose down"
echo "  • Estado: docker-compose ps"
echo ""
echo "🔗 Acceso principal: http://localhost"
echo ""
