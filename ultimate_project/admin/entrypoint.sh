#!/bin/bash

# Make the scripts fails if any command fails
set -e

# Create superuser if it does not exist
if [ "${env}" = "prod" ]; then
	cat << EOF | python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
	User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
EOF
fi

python manage.py makemigrations
python manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
