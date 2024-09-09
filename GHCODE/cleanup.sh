#!/bin/bash

# =============================================================================
# SCRIPT DE LIMPIEZA
# Limpia todos los archivos generados por la simulación
# =============================================================================

echo "🧹 LIMPIEZA DE ARCHIVOS DE SIMULACIÓN"
echo "====================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "safe_github_simulator.sh" ]; then
    echo "❌ ERROR: Ejecutar desde el directorio GHCODE/"
    echo "   cd GHCODE && ./cleanup.sh"
    exit 1
fi

echo "📋 Archivos y directorios a limpiar:"
echo "   📁 paqueteria-simulation-fork/"
echo "   📁 test-repo/"
echo "   📄 commit.log (si existe)"
echo ""

# Preguntar confirmación
read -p "¿Eliminar todos los archivos de simulación? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Limpieza cancelada"
    exit 1
fi

echo ""
echo "🧹 Iniciando limpieza..."

# Limpiar fork de simulación
if [ -d "paqueteria-simulation-fork" ]; then
    echo "   🗑️  Eliminando paqueteria-simulation-fork/"
    rm -rf paqueteria-simulation-fork
    echo "   ✅ Eliminado"
else
    echo "   ℹ️  paqueteria-simulation-fork/ no existe"
fi

# Limpiar repositorio de prueba
if [ -d "test-repo" ]; then
    echo "   🗑️  Eliminando test-repo/"
    rm -rf test-repo
    echo "   ✅ Eliminado"
else
    echo "   ℹ️  test-repo/ no existe"
fi

# Limpiar archivos temporales
if [ -f "commit.log" ]; then
    echo "   🗑️  Eliminando commit.log"
    rm -f commit.log
    echo "   ✅ Eliminado"
else
    echo "   ℹ️  commit.log no existe"
fi

echo ""
echo "✅ LIMPIEZA COMPLETADA"
echo "   Todos los archivos de simulación han sido eliminados"
echo "   Los scripts originales se mantienen intactos"
