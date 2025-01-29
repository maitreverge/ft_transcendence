#!/bin/bash
python manage.py collectstatic --noinput
chmod -R 777 /app/staticfiles
exec "$@"