#!/bin/bash

# Make the scripts fails if any command fails
set -e

# cat << EOF | python3 manage.py shell
# from django.contrib.auth import get_user_model

# User = get_user_model()
# if not User.objects.filter(is_superuser=True).exists():
#     User.objects.create_superuser(username='admin', password='admin', email='admin@email.com')
#     print("Superuser created.")
# else:
#     print("Superuser already exists.")
# EOF

python3 manage.py makemigrations

python3 manage.py migrate --database=users
python3 manage.py migrate --database=matches
python3 manage.py migrate --database=tournaments

python3 manage.py migrate

# Create superuser if it does not exist
if [ -z "$(python3 manage.py shell -c 'from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())')" ]; then
    python3 manage.py createsuperuser --noinput
fi


if [ "${env}" = "prod" ]; then \
	mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
	python3 manage.py collectstatic --noinput; \
	uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
	python3 ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"
