#!/bin/bash

# Make the scripts fails if any command fails
set -e


python3 manage.py migrate --noinput

# Ensure a superuser exists (only run this AFTER migrations)
python3 manage.py shell -c "
from django.db import connection
from django.contrib.auth import get_user_model;

# Check if auth_user table exists before querying
with connection.cursor() as cursor:
    cursor.execute(\"SELECT to_regclass('auth_user')\")
    exists = cursor.fetchone()[0]

if exists:
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin@example.com', 'admin', 'adminpassword')
"

yes | python3 manage.py makemigrations auth_app
yes | python3 manage.py makemigrations user_management_app

python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python3 manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python3 ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
