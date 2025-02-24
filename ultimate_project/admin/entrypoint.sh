#!/bin/bash
yes | python3 manage.py makemigrations
python3 manage.py migrate

if [ "$(python3 manage.py shell -c 'from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())')" = "False" ]; then
	python3 manage.py createsuperuser --noinput
fi

yes | python3 manage.py makemigrations
python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python3 manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python3 ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
