# 🚀 GHCODE - Simulador de Commits para Paquetería

Esta carpeta contiene herramientas para simular un historial de commits realista para el proyecto Paquetería.

## 📁 Archivos Incluidos

### Scripts de Simulación

- **`safe_github_simulator.sh`** - Simulador principal que clona el repo real y genera commits
- **`test_commits.sh`** - Script básico de prueba para commits locales
- **`simulate_paqueteria_commits.sh`** - Simulador original con estructura básica

### Características

- ✅ **8 meses de historial** de commits simulados
- ✅ **Archivos reales** del proyecto Paquetería
- ✅ **Mensajes de commit** específicos del proyecto
- ✅ **Seguro** - No afecta el repositorio original
- ✅ **Realista** - Simula patrones de desarrollo reales

## 🚀 Uso Rápido

```bash
# Ejecutar simulación completa (8 meses)
./safe_github_simulator.sh

# Ver resultados
cd paqueteria-simulation-fork
git log --oneline --graph
```

## 📊 Estadísticas Esperadas

- **Período**: 8 meses (240 días aproximadamente)
- **Commits por día**: 1-4 (70% probabilidad)
- **Total estimado**: ~500-800 commits
- **Archivos simulados**: 10 archivos principales del proyecto

## 🛡️ Seguridad

- ✅ Trabaja con fork local del repositorio
- ✅ No modifica el repositorio original
- ✅ Validaciones de seguridad incluidas
- ✅ Fácil limpieza con `rm -rf paqueteria-simulation-fork`

## 🔧 Configuración

El script está configurado para:
- **Repositorio**: https://github.com/jveyes/Paqueteria.git
- **Período**: Últimos 8 meses
- **Archivos**: Estructura real del proyecto
- **Mensajes**: Específicos para Paquetería

## 📈 Resultados

Después de la simulación tendrás:
- Fork local con historial completo
- Estadísticas de commits
- Gráficos de actividad
- Comandos útiles para inspección

---

**Versión**: 1.0  
**Fecha**: Enero 2025  
**Autor**: Equipo PAPYRUS  
**Propósito**: Simulación de historial de commits para análisis y testing
