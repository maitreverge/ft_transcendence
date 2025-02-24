#!/bin/bash

# Make the scripts fails if any command fails
set -e

# ! ============= TESTING STUFF, DO NOT COPY ====================

# I need to make sure old migrations do not interact with db data stuff


# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete

# ! ============= TESTING STUFF, DO NOT COPY ====================

# Apply database migrations
# ! IMPORTANT : You need to create a new `makemigrations` rule for every app
# ! You also need to pipe it in the 'yes' command to avoid prompting confirmation

# yes | python3 manage.py makemigrations
# python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python3 manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python3 ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
