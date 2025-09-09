#!/bin/bash

# =============================================================================
# EJECUTOR PRINCIPAL DE SIMULACIÓN
# Ejecuta la simulación completa y muestra estadísticas
# =============================================================================

echo "🚀 INICIANDO SIMULACIÓN COMPLETA DE PAQUETERÍA"
echo "=============================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "safe_github_simulator.sh" ]; then
    echo "❌ ERROR: Ejecutar desde el directorio GHCODE/"
    echo "   cd GHCODE && ./run_simulation.sh"
    exit 1
fi

# Hacer ejecutable el script principal
chmod +x safe_github_simulator.sh

echo "📋 Configuración de la simulación:"
echo "   📅 Período: Últimos 8 meses"
echo "   📦 Repositorio: jveyes/Paqueteria"
echo "   🎯 Objetivo: ~500-800 commits simulados"
echo ""

# Preguntar confirmación
read -p "¿Continuar con la simulación? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Simulación cancelada"
    exit 1
fi

echo ""
echo "🚀 Ejecutando simulación..."
echo ""

# Ejecutar la simulación
./safe_github_simulator.sh

# Verificar si la simulación fue exitosa
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SIMULACIÓN COMPLETADA EXITOSAMENTE"
    echo "====================================="
    
    # Mostrar estadísticas adicionales
    if [ -d "paqueteria-simulation-fork" ]; then
        cd paqueteria-simulation-fork
        
        echo ""
        echo "📊 ESTADÍSTICAS FINALES:"
        echo "========================"
        echo "Total de commits: $(git rev-list --count HEAD)"
        echo "Archivos en el repo: $(git ls-files | wc -l)"
        echo "Primer commit: $(git log --reverse --pretty=format:'%ad' --date=short | head -1)"
        echo "Último commit: $(git log --pretty=format:'%ad' --date=short | head -1)"
        
        echo ""
        echo "📈 ACTIVIDAD POR MES:"
        echo "===================="
        git log --pretty=format:'%ad' --date=format:'%Y-%m' | sort | uniq -c | sort -k2
        
        echo ""
        echo "🔍 COMANDOS ÚTILES:"
        echo "=================="
        echo "Ver historial: git log --oneline --graph"
        echo "Ver estadísticas: git log --stat"
        echo "Ver cambios: git show HEAD"
        echo "Salir del fork: cd .."
        
        cd ..
    fi
    
    echo ""
    echo "🎉 ¡Simulación completada!"
    echo "   📁 Fork local: paqueteria-simulation-fork/"
    echo "   🧹 Para limpiar: rm -rf paqueteria-simulation-fork"
    
else
    echo ""
    echo "❌ ERROR EN LA SIMULACIÓN"
    echo "   Revisar logs anteriores para más detalles"
    exit 1
fi
