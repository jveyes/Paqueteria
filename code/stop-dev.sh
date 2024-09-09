#!/bin/bash

echo "🛑 Parando entorno de desarrollo..."

# Parar servicios
docker-compose -f docker-compose.dev.yml down

echo "✅ Entorno de desarrollo detenido!"
echo ""
echo "💡 Para iniciar: ./start-dev.sh"
