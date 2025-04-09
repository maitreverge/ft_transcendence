#! /bin/sh

# Stop dockers
docker compose stop

# Grant permission to remove files
chown $USER:$USER ./databaseapi/databaseapi_app/migrations/0002*.py
chown $USER:$USER ./databaseapi/databaseapi_app/migrations/0003*.py
chown $USER:$USER ./databaseapi/databaseapi_app/migrations/0004*.py

# Delete migrations
rm -rf ./databaseapi/databaseapi_app/migrations/0002*.py
rm -rf ./databaseapi/databaseapi_app/migrations/0003*.py
rm -rf ./databaseapi/databaseapi_app/migrations/0004*.py

# Launch an Ubuntu container attaching to the volume at the root
docker run --rm -it -v ~/volumes_transcendence:/mnt ubuntu bash

# Delete the container from within the container...
rm -rf /mnt/postgres

# ... then exit the container
exit

