#!/bin/bash

if [ "${env}" = "prod" ]; then
	python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
	if not User.objects.filter(username='admin').exists(): \
		User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
fi

yes | python3 manage.py makemigrations
python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python3 manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python3 ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
