#!/usr/bin/env bash
# start.sh: ejecutar migraciones y arrancar Gunicorn en Render

echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando servidor con Gunicorn..."
gunicorn sygnasis_project.wsgi:application --bind 0.0.0.0:10000
