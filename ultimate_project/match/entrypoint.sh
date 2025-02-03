#!/bin/bash

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
	uvicorn match.asgi:application --host 0.0.0.0 --port 8002; \
else \
	python ./manage.py runserver 0.0.0.0:8002; \
fi

exec "$@"