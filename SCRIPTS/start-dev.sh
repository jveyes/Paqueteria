#!/bin/bash

echo "🚀 Iniciando entorno de desarrollo..."

# Verificar que Docker esté ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está ejecutándose. Por favor inicia Docker primero."
    exit 1
fi

# Parar servicios existentes si están ejecutándose
echo "🛑 Parando servicios existentes..."
docker-compose -f docker-compose.dev.yml down

# Construir solo si es necesario
echo "🔨 Construyendo contenedores..."
docker-compose -f docker-compose.dev.yml build

# Iniciar servicios
echo "▶️  Iniciando servicios..."
docker-compose -f docker-compose.dev.yml up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado
echo "📊 Estado de los servicios:"
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "✅ Entorno de desarrollo iniciado!"
echo "🌐 Aplicación: http://localhost"
echo "🔧 API: http://localhost:8000"
echo "📊 Logs: docker-compose -f docker-compose.dev.yml logs -f"
echo ""
echo "💡 Para parar: ./stop-dev.sh"
