#!/bin/bash

# Make the scripts fails if any command fails
set -e

# Apply database migrations
# ! IMPORTANT : You need to create a new `makemigrations` for every app
python3 manage.py makemigrations auth_app
python3 manage.py makemigrations user_management_app
python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
