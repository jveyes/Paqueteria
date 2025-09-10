#!/bin/bash

echo "🔄 Reiniciando entorno de desarrollo..."

# Parar servicios
docker-compose -f docker-compose.dev.yml down

# Iniciar servicios
docker-compose -f docker-compose.dev.yml up -d

# Esperar a que estén listos
sleep 5

echo "✅ Entorno de desarrollo reiniciado!"
echo "🌐 Aplicación: http://localhost"
