#!/bin/bash

# =============================================================================
# SCRIPT DE PRUEBA PARA GENERACIÓN DE COMMITS
# ⚠️  SOLO PARA PRUEBAS LOCALES - NO USAR EN REPOSITORIOS REALES
# =============================================================================

# --- CONFIGURACIÓN ---
# 1. Repositorio de prueba LOCAL (no remoto)
REPO_NAME="test-repo"

# 2. Fechas (formato YYYY-MM-DD). Por defecto, últimos 7 días para prueba rápida.
START_DATE=$(date -d "7 days ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

# 3. Nombre del archivo temporal para los commits.
FILENAME="commit.log"

# 4. Directorio de trabajo
WORK_DIR="/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/GHCODE"

echo "=========================================="
echo "🧪 SCRIPT DE PRUEBA - COMMITS"
echo "=========================================="
echo "📁 Directorio de trabajo: $WORK_DIR"
echo "📅 Rango de fechas: $START_DATE a $END_DATE"
echo "📦 Repositorio de prueba: $REPO_NAME"
echo "=========================================="

# Cambiar al directorio de trabajo
cd "$WORK_DIR"

# --- LÓGICA DEL SCRIPT ---

# Crear repositorio de prueba local (si no existe)
if [ -d "$REPO_NAME" ]; then
  echo "📂 Repositorio de prueba ya existe, entrando..."
  cd "$REPO_NAME"
else
  echo "📂 Creando repositorio de prueba local..."
  mkdir "$REPO_NAME"
  cd "$REPO_NAME"
  git init
  echo "# Repositorio de Prueba para Commits" > README.md
  git add README.md
  git commit -m "Initial commit - test repository"
  echo "✅ Repositorio de prueba inicializado"
fi

# Inicia un bucle desde la fecha de inicio hasta la fecha de fin
current_date=$(date -d "$START_DATE" +%s)
end_date_s=$(date -d "$END_DATE" +%s)

echo ""
echo "🚀 Iniciando la generación de commits de prueba..."
echo ""

total_commits=0
total_days=0

while [ "$current_date" -le "$end_date_s" ]; do
  # Formatea la fecha para el commit
  commit_date=$(date -d "@$current_date" --iso-8601=seconds)
  day_name=$(date -d "@$current_date" +%Y-%m-%d)
  echo "📅 Procesando fecha: $day_name"

  # Decide si se hará un commit este día (80% de probabilidad para simular días libres)
  if [ $(($RANDOM % 10)) -lt 8 ]; then
    # Genera un número aleatorio de commits para este día (entre 1 y 5 para prueba rápida)
    num_commits=$((($RANDOM % 5) + 1))
    
    echo "   📝 Generando $num_commits commits para $day_name"

    for (( i=1; i<=$num_commits; i++ )); do
      # Escribe algo en el archivo para que haya un cambio que commitear
      echo "$commit_date - commit #$i - Test data $(date +%s)" >> $FILENAME

      # Agrega el archivo al staging
      git add $FILENAME

      # Realiza el commit con la fecha
      GIT_COMMITTER_DATE="$commit_date" GIT_AUTHOR_DATE="$commit_date" git commit -m "chore: test commit for $day_name (#$i)" > /dev/null 2>&1
      
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
echo "✅ Generación de commits completada"
echo "📊 Estadísticas:"
echo "   📅 Días procesados: $total_days"
echo "   📝 Total de commits: $total_commits"
echo "   📁 Repositorio: $(pwd)"
echo "=========================================="

# Mostrar el historial de commits
echo ""
echo "📋 Historial de commits generado:"
echo "----------------------------------------"
git log --oneline --graph --decorate -10

echo ""
echo "🔍 Comandos útiles para inspeccionar:"
echo "   git log --oneline --graph --all"
echo "   git log --pretty=format:'%h %ad %s' --date=short"
echo "   git show --stat"

echo ""
echo "⚠️  NOTA: Este es solo un repositorio de prueba local."
echo "   No se ha subido a ningún repositorio remoto."
echo "   Para limpiar: rm -rf $REPO_NAME"
