#!/bin/bash

# python3 manage.py migrate --run-syncdb
python3 manage.py makemigrations databaseapi_app
python3 manage.py makemigrations
python3 manage.py migrate

# ! OLD SUPER USER SCRIPT CREATION
# Ensure a superuser exists
# python3 manage.py shell -c "
# from django.contrib.auth import get_user_model;
# User = get_user_model()
# if not User.objects.filter(is_superuser=True).exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin')
# "

# Create users in the user.csv file
# python3 _docker/init_users.py
# python3 _docker/init_users.py
# python3 _docker/init_users.py
# python3 manage.py shell -c "exec(open('_docker/init_users.py').read())"
# First, place your script in a scripts directory
# First make sure django-extensions is installed
# Then, put your script in a 'scripts' directory in your app
python3 manage.py runscript init_users

python3 manage.py makemigrations databaseapi_app
python3 manage.py makemigrations
python3 manage.py migrate

if [ "${env}" = "prod" ]; then \
    mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
    python3 manage.py collectstatic --noinput; \
    uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
    python3 ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"