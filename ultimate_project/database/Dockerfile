FROM postgres:latest

# Add the initialization SQL script to the Docker image
COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432