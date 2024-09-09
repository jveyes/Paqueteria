# ========================================
# PAQUETES EL CLUB v3.5 - Dockerfile Optimizado para Producción
# ========================================

# Multi-stage build para optimizar tamaño de imagen
FROM python:3.11-slim as builder

# Instalar dependencias del sistema necesarias para compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --user -r requirements.txt

# ========================================
# Imagen final optimizada
# ========================================
FROM python:3.11-slim

# Instalar dependencias del sistema para runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código de la aplicación
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY *.sql ./

# Crear directorios necesarios
RUN mkdir -p logs uploads database/backups && \
    chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Agregar directorio de dependencias al PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
