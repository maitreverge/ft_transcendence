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





# #! /bin/bash

# # Ensure the database exists
# psql -U "$POSTGRES_USER" -c "CREATE DATABASE ${POSTGRES_DB:-trans_db};"

# # Create an additional admin user
# psql -U "$POSTGRES_USER" -c "CREATE USER ${POSTGRES_ADMIN:-admin} WITH PASSWORD '${ADMIN_PASSWORD:-adminpassword}';"

# # Grant all privileges to the new admin user
# psql -U "$POSTGRES_USER" -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB:-trans_db} TO ${POSTGRES_ADMIN:-admin};"

# # Allow the new admin user to create new databases
# psql -U "$POSTGRES_USER" -c "ALTER USER ${POSTGRES_ADMIN:-admin} CREATEDB;"

# # Grant privileges on public schema
# psql -U "$POSTGRES_USER" -c "GRANT ALL ON SCHEMA public TO ${POSTGRES_ADMIN:-admin};"
