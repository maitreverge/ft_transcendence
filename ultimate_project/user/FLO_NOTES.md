✅
⛔
🟧 

--------------------------------------------------------------------------------
MY STUFF
--------------------------------------------------------------------------------
http://localhost:8000/user/
http://localhost:8000/auth/  ==>  redirect to http://localhost:8000/auth/login/



## DATABASE PORTS

- "5433:5432"  => USER_DB
- "5434:5432"  => 
- "5435:5432"  => 
- "5436:5432"  => 
- "5437:5432"  => 


--------------------------------------------------------------------------------
TO ASK
--------------------------------------------------------------------------------


- Shift from `-environment` to `-env_file` in compose ?
- Make the posgreSQL works with the compose-prod

--------------------------------------------------------------------------------
WIP
--------------------------------------------------------------------------------
## DB linking with Postgres :

- Now `admin` container if OFF + desactivate nginx routes

- Test admin inside users
- Test creating stuff with user admin
- Restart containers and check


Container `users` with an admin makes the build crash
- Need to fix ngninx with healchecks

IMPORTANT :
When in a multi DB environment, migrations applies to the default, we need to specify which migration we need to make

--------------------------------------------------------------------------------
TOUDOU LIST
--------------------------------------------------------------------------------
# TO FIX :
- Write all healths checks for all django containers

# MULTIPLES DATABASE CONTAINERS :

- ⛔ Automate scripting for creating db
- ⛔ Create bind mounts on a a single folder which contains all sub folder related to every database
- ⛔ Create multiple postgres containers with a related docker-compose
- ⛔ Create SIMPLE models without foreigns keys + Migrate + modify + delete them inside the Djangos apps
- ⛔ Connect every containers which contains models to every others dbs
- ⛔ Connect each database to the host on a different port, but keep the same port for the docker network
- ⛔ 
- ⛔ 


# PRIORITY :
- ✅ Create a dummy model + Connect A regular container to the DB
- ⛔ Connect Django Admin to the DB
- ⛔ Make Django Admin connect to the db and write in it (double check with SQL queries straight in the container)
- ⛔ Connect another container with another models
- ⛔ Connect another model to the DB, and with Django Admin again

- Write doc on what to change for others (migrations, ect...)

# PRIORITY :

--------------------------------------------------------------------------------
TO SEARCH
--------------------------------------------------------------------------------
- Django Password Hashers : https://docs.djangoproject.com/fr/2.2/topics/auth/passwords/

--------------------------------------------------------------------------------





--------------------------------------------------------------------------------
DUMP
--------------------------------------------------------------------------------
