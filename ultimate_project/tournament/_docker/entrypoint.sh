#!/bin/bash

# Make the scripts fails if any command fails
set -e

# Apply database migrations
# ! IMPORTANT : You need to create a new `makemigrations` for every app

python manage.py makemigrations tournament_app
python manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
