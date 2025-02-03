#!/bin/bash

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
	uvicorn tournament.asgi:application --host 0.0.0.0 --port 8001; \
else \
	python ./manage.py runserver 0.0.0.0:8001; \
fi

exec "$@"