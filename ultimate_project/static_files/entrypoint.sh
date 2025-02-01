#!/bin/bash

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python manage.py collectstatic --noinput; \
	uvicorn static_files.asgi:application --host 0.0.0.0 --port 8000; \
else \
	python ./manage.py runserver 0.0.0.0:8000; \
fi

exec "$@"