#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.5 - Script de Despliegue para Producción
# ========================================

set -e  # Salir en caso de error

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
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Función para verificar prerrequisitos
check_prerequisites() {
    log "Verificando prerrequisitos..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado"
        exit 1
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose no está instalado"
        exit 1
    fi
    
    # Verificar archivo .env
    if [[ ! -f "$PROJECT_DIR/.env" ]]; then
        error "Archivo .env no encontrado"
        exit 1
    fi
    
    success "Prerrequisitos verificados"
}

# Función para crear backup
create_backup() {
    log "Creando backup de la versión actual..."
    
    BACKUP_DIR="$PROJECT_DIR/BACKUPS"
    mkdir -p "$BACKUP_DIR"
    
    # Backup de volúmenes Docker
    if docker volume ls | grep -q "paqueteria_v35_redis_data"; then
        docker run --rm -v paqueteria_v35_redis_data:/data -v "$BACKUP_DIR":/backup alpine tar czf "/backup/redis_data_${TIMESTAMP}.tar.gz" -C /data .
        success "Backup de Redis creado"
    fi
    
    success "Backup completado"
}

# Función para detener servicios
stop_services() {
    log "Deteniendo servicios actuales..."
    
    cd "$PROJECT_DIR"
    
    if docker-compose ps | grep -q "Up"; then
        docker-compose down
        success "Servicios detenidos"
    else
        warning "No hay servicios corriendo"
    fi
}

# Función para limpiar recursos Docker
cleanup_docker() {
    log "Limpiando recursos Docker no utilizados..."
    
    # Limpiar contenedores detenidos
    docker container prune -f
    
    # Limpiar imágenes no utilizadas
    docker image prune -f
    
    # Limpiar redes no utilizadas
    docker network prune -f
    
    success "Limpieza completada"
}

# Función para construir y levantar servicios
start_services() {
    log "Construyendo y levantando servicios..."
    
    cd "$PROJECT_DIR"
    
    # Construir imágenes
    log "Construyendo imágenes Docker..."
    docker-compose build --no-cache
    
    # Levantar servicios
    log "Levantando servicios..."
    docker-compose up -d
    
    success "Servicios levantados"
}

# Función para health checks
health_checks() {
    log "Realizando health checks..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log "Health check intento $attempt/$max_attempts"
        
        # Verificar que todos los contenedores estén corriendo
        if ! docker-compose ps | grep -q "Up"; then
            warning "Algunos contenedores no están corriendo"
            sleep 10
            ((attempt++))
            continue
        fi
        
        # Verificar health endpoints
        if curl -f -s "http://localhost/health" > /dev/null 2>&1; then
            success "Health check exitoso"
            return 0
        fi
        
        sleep 10
        ((attempt++))
    done
    
    error "Health check falló después de $max_attempts intentos"
    return 1
}

# Función para verificar logs
check_logs() {
    log "Verificando logs de servicios..."
    
    cd "$PROJECT_DIR"
    
    # Verificar logs de la aplicación
    log "Verificando logs de la aplicación..."
    app_logs=$(docker-compose logs app --tail=50)
    
    if echo "$app_logs" | grep -i "error\|exception\|traceback" | grep -v "DEBUG" > /dev/null; then
        warning "Errores encontrados en logs de la aplicación:"
        echo "$app_logs" | grep -i "error\|exception\|traceback" | grep -v "DEBUG" | head -10
    else
        success "Logs de aplicación sin errores críticos"
    fi
    
    # Verificar logs de nginx
    log "Verificando logs de nginx..."
    nginx_logs=$(docker-compose logs nginx --tail=20)
    
    if echo "$nginx_logs" | grep -i "error" > /dev/null; then
        warning "Errores encontrados en logs de nginx:"
        echo "$nginx_logs" | grep -i "error" | head -5
    else
        success "Logs de nginx sin errores críticos"
    fi
}

# Función para mostrar estado final
show_status() {
    log "Estado final de servicios:"
    
    cd "$PROJECT_DIR"
    docker-compose ps
    
    echo ""
    log "URLs de acceso:"
    echo "  🌐 HTTP:  http://localhost"
    echo "  🔒 HTTPS: https://localhost (requiere certificados SSL)"
    echo "  📊 Health: http://localhost/health"
    echo "  📚 API Docs: http://localhost/docs"
    echo "  📈 Prometheus: http://localhost:9090"
    echo "  📊 Grafana: http://localhost:3000"
    
    echo ""
    log "Comandos útiles:"
    echo "  📋 Ver logs: docker-compose logs -f"
    echo "  🔄 Reiniciar: docker-compose restart"
    echo "  🛑 Detener: docker-compose down"
    echo "  📊 Estado: docker-compose ps"
}

# Función principal
main() {
    echo "=========================================="
    echo "🚀 DESPLIEGUE PRODUCCIÓN - PAQUETES EL CLUB v3.5"
    echo "=========================================="
    echo ""
    
    # Ejecutar pasos de despliegue
    check_prerequisites
    create_backup
    stop_services
    cleanup_docker
    start_services
    health_checks || exit 1
    check_logs
    show_status
    
    echo ""
    success "🎉 Despliegue completado exitosamente!"
    echo ""
    echo "📋 Resumen:"
    echo "  • Backup creado"
    echo "  • Servicios reiniciados"
    echo "  • Health checks pasados"
    echo "  • Funcionalidad verificada"
    echo ""
    echo "🔗 Acceso: http://localhost"
    echo ""
    echo "📝 Logs disponibles con: docker-compose logs -f"
}

# Función para manejo de errores
error_handler() {
    local exit_code=$?
    local line_number=$1
    
    echo ""
    error "❌ Error en línea $line_number (código: $exit_code)"
    echo ""
    echo "🔧 Pasos para resolver:"
    echo "  1. Verificar logs: docker-compose logs"
    echo "  2. Verificar estado: docker-compose ps"
    echo "  3. Revisar configuración: cat .env"
    echo "  4. Restaurar backup si es necesario"
    echo ""
    
    exit $exit_code
}

# Configurar trap para manejo de errores
trap 'error_handler $LINENO' ERR

# Ejecutar función principal
main "$@"
