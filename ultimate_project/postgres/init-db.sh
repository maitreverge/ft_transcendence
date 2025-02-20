#!/bin/bash
set -e

# Create a superuser
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER superuser WITH SUPERUSER PASSWORD 'superuser_password';
EOSQL

# Grant all privileges on the database to the superuser
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO superuser;
EOSQL

# Additional security settings
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
    ALTER DATABASE $POSTGRES_DB OWNER TO $POSTGRES_USER;
EOSQL