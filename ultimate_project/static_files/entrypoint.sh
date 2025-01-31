#!/bin/bash

python manage.py collectstatic --noinput

if [ "${env}" = "prod" ]; then \
	uvicorn static_files.asgi:application --host 0.0.0.0 --port 8001; \
else \
	python ./manage.py runserver 0.0.0.0:8001; \
fi

exec "$@"