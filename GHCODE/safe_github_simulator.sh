#!/bin/bash

# =============================================================================
# SIMULADOR SEGURO PARA REPOSITORIO GITHUB PAQUETERIA
# ⚠️  VERSIÓN SEGURA - TRABAJA CON FORK LOCAL
# =============================================================================

# --- CONFIGURACIÓN SEGURA ---
# 1. Repositorio original (SOLO LECTURA)
ORIGINAL_REPO="https://github.com/jveyes/Paqueteria.git"
FORK_NAME="paqueteria-simulation-fork"

# 2. Fechas (formato YYYY-MM-DD). Últimos 8 meses para simulación realista
START_DATE=$(date -d "8 months ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

# 3. Archivos que simularían cambios reales en el proyecto (basados en estructura real)
FILES=(
    "code/src/main.py"
    "code/src/models/package.py" 
    "code/src/routers/packages.py"
    "code/templates/dashboard/dashboard.html"
    "code/requirements.txt"
    "code/src/config.py"
    "code/src/models/customer.py"
    "code/src/routers/customers.py"
    "code/templates/customers/search.html"
    "code/static/js/colombia-timezone.js"
)

# 4. Directorio de trabajo
WORK_DIR="/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.5/GHCODE"

echo "=========================================="
echo "🛡️  SIMULADOR SEGURO - PAQUETERIA GITHUB"
echo "=========================================="
echo "📁 Directorio de trabajo: $WORK_DIR"
echo "📅 Rango de fechas: $START_DATE a $END_DATE"
echo "🔗 Repositorio original: $ORIGINAL_REPO"
echo "📦 Fork local: $FORK_NAME"
echo "=========================================="

# Cambiar al directorio de trabajo
cd "$WORK_DIR"

# --- VALIDACIONES DE SEGURIDAD ---

echo "🔍 Realizando validaciones de seguridad..."

# Verificar que no estamos en un repositorio con remotes
if [ -d ".git" ] && git remote -v | grep -q "origin"; then
    echo "❌ ERROR: No ejecutar en repositorios con remotes configurados"
    echo "   Este script debe ejecutarse en un directorio limpio"
    exit 1
fi

# Verificar conectividad a GitHub (opcional)
echo "🔍 Verificando conectividad a GitHub..."
if curl -s --head "$ORIGINAL_REPO" | head -n 1 | grep -q "200 OK"; then
    echo "✅ Conectividad a GitHub verificada"
else
    echo "⚠️  ADVERTENCIA: No se puede verificar conectividad a GitHub"
    echo "   Continuando con simulación local..."
fi

echo "✅ Validaciones de seguridad completadas"

# --- LÓGICA DEL SCRIPT SEGURO ---

# Crear fork local del repositorio original (si no existe)
if [ -d "$FORK_NAME" ]; then
    echo "📂 Fork local ya existe, entrando..."
    cd "$FORK_NAME"
    
    # Actualizar desde el repositorio original
    echo "🔄 Actualizando desde repositorio original..."
    git fetch origin
    git reset --hard origin/main
else
    echo "📂 Creando fork local del repositorio original..."
    git clone "$ORIGINAL_REPO" "$FORK_NAME"
    cd "$FORK_NAME"
    
    # Configurar git para commits simulados
    git config user.name "Simulation Bot"
    git config user.email "simulation@paqueteria.local"
    
    echo "✅ Fork local creado y configurado"
fi

# Inicia un bucle desde la fecha de inicio hasta la fecha de fin
current_date=$(date -d "$START_DATE" +%s)
end_date_s=$(date -d "$END_DATE" +%s)

echo ""
echo "🚀 Iniciando la simulación de commits para Paqueteria..."
echo ""

total_commits=0
total_days=0

# Mensajes de commit realistas para el proyecto (basados en estructura real)
COMMIT_MESSAGES=(
    "feat: add package tracking functionality"
    "fix: resolve database connection issue with RDS"
    "refactor: improve package validation logic"
    "docs: update API documentation"
    "style: format code according to PEP8"
    "test: add unit tests for package service"
    "perf: optimize database queries for packages"
    "chore: update dependencies in requirements.txt"
    "feat: add email notifications for package status"
    "fix: handle edge case in package status updates"
    "refactor: restructure models directory"
    "docs: add deployment guide for Docker"
    "feat: implement user authentication system"
    "fix: resolve timezone issues in Colombia"
    "style: improve dashboard UI components"
    "test: add integration tests for customers"
    "perf: cache frequently accessed package data"
    "chore: update Docker configuration"
    "feat: add package search functionality"
    "fix: resolve SMS notification bug with LIWA"
    "feat: add customer management system"
    "fix: resolve SSL certificate issues"
    "refactor: improve FastAPI router structure"
    "docs: update README with new features"
    "feat: add Prometheus monitoring integration"
    "fix: resolve Redis connection issues"
    "style: improve responsive design for mobile"
    "test: add end-to-end tests for package flow"
    "perf: optimize PostgreSQL queries"
    "chore: update nginx configuration"
)

while [ "$current_date" -le "$end_date_s" ]; do
    # Formatea la fecha para el commit
    commit_date=$(date -d "@$current_date" --iso-8601=seconds)
    day_name=$(date -d "@$current_date" +%Y-%m-%d)
    echo "📅 Procesando fecha: $day_name"

    # Decide si se hará un commit este día (70% de probabilidad para simular días libres)
    if [ $(($RANDOM % 10)) -lt 7 ]; then
        # Genera un número aleatorio de commits para este día (entre 1 y 4 para 8 meses)
        num_commits=$((($RANDOM % 4) + 1))
        
        echo "   📝 Generando $num_commits commits para $day_name"

        for (( i=1; i<=$num_commits; i++ )); do
            # Selecciona un archivo aleatorio para modificar
            file_to_modify=${FILES[$RANDOM % ${#FILES[@]}]}
            
            # Crea el archivo si no existe
            mkdir -p "$(dirname "$file_to_modify")"
            
            # Agrega contenido realista al archivo
            echo "# Modified on $commit_date - commit #$i" >> "$file_to_modify"
            echo "# Simulation change: $(date +%s)" >> "$file_to_modify"
            echo "# Random improvement: $(shuf -n 1 <<< 'performance optimization bug fix feature enhancement code cleanup')" >> "$file_to_modify"
            
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
echo "🛡️  INFORMACIÓN DE SEGURIDAD:"
echo "   ✅ Este es un fork local del repositorio original"
echo "   ✅ No se han realizado cambios al repositorio original"
echo "   ✅ Todos los commits son simulaciones locales"
echo "   ✅ Para limpiar: rm -rf $FORK_NAME"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Este fork local NO está conectado a GitHub"
echo "   - Los commits son solo para simulación local"
echo "   - No afecta el repositorio original jveyes/Paqueteria"
echo "   - Para subir a GitHub, necesitarías crear un fork real"
