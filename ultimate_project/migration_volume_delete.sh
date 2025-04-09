#! /bin/sh

# Make sure containers are stopped
docker compose stop

# Launch an Ubuntu container and delete the volume from within the container
docker run --rm -v ~/volumes_transcendence:/mnt ubuntu bash -c "rm -rf /mnt/postgres && echo 'Postgres volume deleted successfully'"