✅
⛔
🟧 

--------------------------------------------------------------------------------
MY ROUTES
--------------------------------------------------------------------------------
http://localhost:8000/user/
http://localhost:8000/auth/  ==>  redirect to http://localhost:8000/auth/login/



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

--------------------------------------------------------------------------------
TOUDOU LIST
--------------------------------------------------------------------------------
# TO FIX :
- Make ngnix start after all containers are healthy


# PRIORITY :
- ⛔ Create a dummy model + Connect A regular container to the DB
- ⛔ Connect Django Admin to the DB
- ⛔ Make Django Admin connect to the db and write in it (double check with SQL queries straight in the container)
- ⛔ Connect another container with another models
- ⛔ Connect another model to the DB, and with Django Admin again

- Write doc on what to change for others (migrations, ect...)


--------------------------------------------------------------------------------
TO SEARCH
--------------------------------------------------------------------------------
- Django Password Hashers : https://docs.djangoproject.com/fr/2.2/topics/auth/passwords/

--------------------------------------------------------------------------------





--------------------------------------------------------------------------------
DUMP
--------------------------------------------------------------------------------
