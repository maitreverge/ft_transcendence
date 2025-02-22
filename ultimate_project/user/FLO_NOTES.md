✅
⛔
🟧
⚠️
--------------------------------------------------------------------------------
									DUMP IDEAS
--------------------------------------------------------------------------------



--------------------------------------------------------------------------------
									MY ROUTES
--------------------------------------------------------------------------------
http://localhost:8000/user/
http://localhost:8000/auth/  ==>  redirect to http://localhost:8000/auth/login/




--------------------------------------------------------------------------------
									DATABASE
--------------------------------------------------------------------------------

## DATABASE PORTS

- "5434:5432"  => USER_DB
- "5435:5432"  => TOURNAMENT_DB
- "5436:5432"  => MATCH_DB
- "5436:5432"  => 


--------------------------------------------------------------------------------
									TO ASK
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
									WIP
--------------------------------------------------------------------------------
## DB linking with Postgres :

- Now `admin` container if OFF + desactivated related `nginx` routes


⚠️⚠️⚠️⚠️⚠️⚠️ IMPORTANT ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️ :
When in a multi DB environment, migrations applies to the `default`,we need to specify which migration we need to make

--------------------------------------------------------------------------------
									TOUDOU LIST
--------------------------------------------------------------------------------
# TO FIX LATER :
- DB containers actually create folders of the same service name
- Potentially shell scripting Automate `makemigrations` on each new app created

# MULTIPLES DATABASE CONTAINERS :

- ✅ Create bind mounts on a a single folder which contains all sub folder related to every database
- ✅ Create multiple postgres containers with a related docker-compose
- ✅ Create SIMPLE models without foreigns keys + Migrate + modify + delete them inside the Djangos apps
- ✅ Connect every containers which contains models to every others dbs
- ✅ Connect each database to the host on a different port, but keep the same port for the docker network

# 🪡🪡🪡        WORK NEEDLE        🪡🪡🪡🪡🪡🪡
ONE CONTAINER CONNECTING TO MULTIPLE DATABASES
- ⛔ Connect `user` to both `user_db` and `match_db` in `user.settings.py`
- ⛔ Create a Model in User with a Foreign key
- ⛔ Create A few data for `match_db`
- ⛔ Create data in `user_db` fetching data from `match_db`

For data simplicity manipulation
- ⛔ Connect Django Admin to all DBs


# PRIORITY :
- ✅ Create a dummy model + Connect A regular container to the DB
- ⛔ Make Django Admin connect to the db and write in it (double check with SQL queries straight in the container)
- ⛔ Connect another container with another models
- ⛔ Connect another model to the DB, and with Django Admin again

- Write doc on what to change for others (migrations, ect...)


--------------------------------------------------------------------------------
								TO SEARCH  // DOC
--------------------------------------------------------------------------------
- Django Password Hashers : https://docs.djangoproject.com/fr/2.2/topics/auth/passwords/



