✅
⛔
🟧
⚠️
--------------------------------------------------------------------------------
									DUMP IDEAS
--------------------------------------------------------------------------------

⛔ ✅  

# PRIORITY

## DATABASE ENTRYPOINTS

⛔ ✅  Split `admin` id from the `Players` logic to avoid getting disconnected
⛔ ✅  Strip every cipher / encryption logic into the `database_api` container
⛔ ✅  Optimize `entrypoint.sh` for  `database_api`
⛔ ✅  


## DATABASE ENTRYPOINTS
⛔ ✅  Start making endpoints
⛔ ✅  





⛔ ✅  Possibly leverage django filters


⛔ ✅ centraliser la documentation django / database / container

--------------------------------------------------------------------------------
									MY ROUTES
--------------------------------------------------------------------------------

http://localhost:8000/admin/  ==>  ADMIN PANEL



--------------------------------------------------------------------------------
									DATABASE
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
									TO ASK
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
									WIP
--------------------------------------------------------------------------------

2FA :
- Implement necessary libraries
- Create interface with Google Authenticator with big ass QR Code
- Make 2FA optional during registering to website (possibily enable it later ?)
- Create a one time password interface when login-in.
- Store + encrypt securely codes ==> `cryptography` module
- LogOut users on 2FA failure.


--------------------------------------------------------------------------------
									TOUDOU LIST
--------------------------------------------------------------------------------
# TO FIX LATER :
⛔ Health tests visible on the console, maybe put them in  `> /dev/null`

⛔ When refreshing AUTH forms, there is a CSRF verification failed.
When


# 🪡🪡🪡        WORK NEEDLE        🪡🪡🪡🪡🪡🪡



--------------------------------------------------------------------------------
								TO SEARCH  // DOC
--------------------------------------------------------------------------------
- Django Password Hashers : https://docs.djangoproject.com/fr/2.2/topics/auth/passwords/


--------------------------------------------------------------------------------
								DONE STUFF
--------------------------------------------------------------------------------

📅  ===== 26-02 =====

- ✅ DB containers actually create folders of the same service name
- ✅ Potentially shell scripting Automate `makemigrations` on each new app created (no need)

- ✅ Create bind mounts on a a single folder which contains all sub folder related to every database
- ✅ Create multiple postgres containers with a related docker-compose
- ✅ Create SIMPLE models without foreigns keys + Migrate + modify + delete them inside the Djangos apps
- ✅ Connect every containers which contains models to every others dbs
- ✅ Connect each database to the host on a different port, but keep the same port for the docker network

ONE CONTAINER CONNECTING TO MULTIPLE DATABASES
- ✅ Connect `user` to both `user_db` and `match_db` in `user.settings.py`
- ✅ Create a Model in User with a Foreign key
- ✅ Create A few data for `match_db`
- ✅ Create data in `user_db` fetching data from `match_db`

For data simplicity manipulation
- ✅ Connect Django Admin to all DBs


# PRIORITY :
- ✅ Create a dummy model + Connect A regular container to the DB
- ✅ Make Django Admin connect to the db and write in it (double check with SQL queries straight in the container)
- ✅ Connect another container with another models
- ✅ Connect another model to the DB, and with Django Admin again


Write basic doc about databases
Clean Repo from database trying
 Fix health test for postgres

📅  ===== 05-03 =====

✅Recheck les BDD avec dbshell dans chaque container
✅ Deplacer les database de /home/ vers racine
✅ Migrer la logique des dockerfiles + la structure global du compose


📅  ===== 06-03 =====

# Migrating models inside a single container
✅  Create a database_api service
✅  Move the managed models in this one
✅  Delete all the others models
✅  Simplify the models ( maybe already simplified )
✅  Remove the healthchecks for old containers
✅  Create the service database_api
✅  Remove the postgres clients from others containers
✅  Roll back to dummy config like
✅  Remove Admin apps in `INSTALLED_APPS`
✅  Remove Database MiddleWares
✅  Remove anything Database Related
✅  Simplify the SQL schemas to have none


📅  ===== 07-03 =====


