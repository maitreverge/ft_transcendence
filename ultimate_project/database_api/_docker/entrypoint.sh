#!/bin/bash

# Check if migration files exist
MIGRATION_EXISTS=$(find /app/database_api_app/migrations -name "0*.py" | wc -l)

if [ "$MIGRATION_EXISTS" -eq 0 ]; then
    # Initial migration needed - no migration files exist
    echo "Creating initial migrations..."
    python3 manage.py makemigrations database_api_app
else
    # Check if there are model changes requiring new migrations
    CHANGES=$(python3 manage.py makemigrations --dry-run --check database_api_app 2>&1)
    if echo "$CHANGES" | grep -q "No changes detected"; then
        echo "No model changes detected, skipping makemigrations"
    else
        echo "Model changes detected, creating migrations..."
        python3 manage.py makemigrations database_api_app
    fi
fi

# Check if there are pending migrations to apply
PENDING_MIGRATIONS=$(python3 manage.py showmigrations --plan | grep -c "\[ \]")
if [ "$PENDING_MIGRATIONS" -gt 0 ]; then
    echo "Applying pending migrations..."
    python3 manage.py migrate
else
    echo "No pending migrations, database is up to date"
fi

# Ensure a superuser exists
python3 manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin@example.com', 'admin', 'adminpassword')
"

if [ "${env}" = "prod" ]; then \
    mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles; \
    python3 manage.py collectstatic --noinput; \
    uvicorn ${name}.asgi:application --host 0.0.0.0 --port ${port}; \
else \
    python3 ./manage.py runserver 0.0.0.0:${port}; \
fi

exec "$@"