#!/bin/bash

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
fi

daphne -b 0.0.0.0 -p ${port} ${name}.asgi:application; \

exec "$@"