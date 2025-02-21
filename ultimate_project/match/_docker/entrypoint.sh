#!/bin/bash

# Make the scripts fails if any command fails
set -e

# Apply database migrations
# ! IMPORTANT : You need to create a new `makemigrations` for every app
python3 manage.py makemigrations match_app
python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
fi

daphne -b 0.0.0.0 -p ${port} ${name}.asgi:application

exec "$@"