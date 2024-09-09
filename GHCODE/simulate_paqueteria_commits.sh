#!/bin/bash

# =============================================================================
# SIMULADOR DE COMMITS PARA REPOSITORIO PAQUETERIA
# ⚠️  SOLO PARA PRUEBAS LOCALES - NO USAR EN REPOSITORIOS REALES
# =============================================================================

# --- CONFIGURACIÓN ---
# 1. Repositorio de prueba basado en Paqueteria
REPO_NAME="paqueteria-test-repo"

# 2. Fechas (formato YYYY-MM-DD). Últimos 30 días para prueba más realista
START_DATE=$(date -d "30 days ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

# 3. Archivos que simularían cambios reales en el proyecto
FILES=("src/main.py" "src/models/package.py" "src/routers/packages.py" "templates/dashboard/dashboard.html" "requirements.txt")

# 4. Directorio de trabajo
WORK_DIR="/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/GHCODE"

echo "=========================================="
echo "📦 SIMULADOR PAQUETERIA - COMMITS"
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
  
  # Crear estructura básica del proyecto
  mkdir -p src/models src/routers templates/dashboard
  touch src/__init__.py src/models/__init__.py src/routers/__init__.py
  
  # Archivo README inicial
  cat > README.md << 'EOF'
# Sistema de Control y Gestión de Paquetes

Sistema desarrollado para el control y gestión de paquetes.

## Características

- Gestión de paquetes
- Dashboard administrativo
- API REST
- Base de datos PostgreSQL

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python src/main.py
```
EOF

  # Archivo requirements.txt inicial
  cat > requirements.txt << 'EOF'
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
EOF

  git add .
  git commit -m "feat: initial project setup"
  echo "✅ Repositorio de prueba inicializado con estructura básica"
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
  "fix: resolve database connection issue"
  "refactor: improve package validation logic"
  "docs: update API documentation"
  "style: format code according to PEP8"
  "test: add unit tests for package service"
  "perf: optimize database queries"
  "chore: update dependencies"
  "feat: add email notifications"
  "fix: handle edge case in package status"
  "refactor: restructure models directory"
  "docs: add deployment guide"
  "feat: implement user authentication"
  "fix: resolve timezone issues"
  "style: improve dashboard UI"
  "test: add integration tests"
  "perf: cache frequently accessed data"
  "chore: update Docker configuration"
  "feat: add package search functionality"
  "fix: resolve SMS notification bug"
)

while [ "$current_date" -le "$end_date_s" ]; do
  # Formatea la fecha para el commit
  commit_date=$(date -d "@$current_date" --iso-8601=seconds)
  day_name=$(date -d "@$current_date" +%Y-%m-%d)
  echo "📅 Procesando fecha: $day_name"

  # Decide si se hará un commit este día (70% de probabilidad para simular días libres)
  if [ $(($RANDOM % 10)) -lt 7 ]; then
    # Genera un número aleatorio de commits para este día (entre 1 y 4)
    num_commits=$((($RANDOM % 4) + 1))
    
    echo "   📝 Generando $num_commits commits para $day_name"

    for (( i=1; i<=$num_commits; i++ )); do
      # Selecciona un archivo aleatorio para modificar
      file_to_modify=${FILES[$RANDOM % ${#FILES[@]}]}
      
      # Crea el archivo si no existe
      mkdir -p "$(dirname "$file_to_modify")"
      
      # Agrega contenido al archivo
      echo "# Modified on $commit_date - commit #$i" >> "$file_to_modify"
      echo "# Random change: $(date +%s)" >> "$file_to_modify"
      
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
echo "⚠️  NOTA: Este es solo un repositorio de prueba local."
echo "   No se ha subido a ningún repositorio remoto."
echo "   Para limpiar: rm -rf $REPO_NAME"
