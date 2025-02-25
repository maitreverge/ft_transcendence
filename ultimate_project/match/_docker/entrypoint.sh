#!/bin/bash

# Make the scripts fails if any command fails
set -e

# Apply database migrations
# ! IMPORTANT : You need to create a new `makemigrations` rule for every app
# ! You also need to pipe it in the 'yes' command to avoid prompting confirmation

yes | python3 manage.py makemigrations
yes | python3 manage.py makemigrations match_app
python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python3 manage.py collectstatic --noinput; \
fi

daphne -b 0.0.0.0 -p ${port} ${name}.asgi:application

exec "$@"