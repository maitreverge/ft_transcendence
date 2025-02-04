#!/bin/bash

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
	daphne -b 0.0.0.0 -p ${port} ${name}.asgi:application; \
else \
	daphne -b 0.0.0.0 -p ${port} ${name}.asgi:application; \
fi

exec "$@"