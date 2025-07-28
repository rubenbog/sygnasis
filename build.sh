#!/usr/bin/env bash
# build.sh

# Instala dependencias y aplica migraciones
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
