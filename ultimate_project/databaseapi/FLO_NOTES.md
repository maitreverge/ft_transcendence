✅
⛔
🟧
⚠️

# BUG REPORT
🟧 404 Quand on clique sur les update formulaires de Thomas
🟧 ACCOUNT THOMAS => Quand on resize la page, les views droppent en bas


--------------------------------------------------------------------------------
									LAST DEV WEEK
--------------------------------------------------------------------------------

🟧 Beautify register / login / 2fa landing pages

🟧 Find a way to lock the database routes as well

⚠️ Lock all the routes (lock les routes visibles dans le front)

🟧 DELETE ALL THE PRINT OF DEBUG WITH SENSITIVE INFOS

🟧 DELETE THIS FLO_NOTES FILES

🟧 DELETE ALL SENSITIVE FILES ON RASPBERRY ENDPOINT, ECT...

🟧 Changer le mot de passe d'admin / Delete l'admin en production (`user_prod.csv`)

🟧 Switch from `user_prod.csv` to `user.csv` in correction 

🟧 https://docs.djangoproject.com/en/5.1/ref/csrf/#csrf-limitations
==> Proteger les routes de POST / PUT / DELETE avec des decorateurs CSRF adequats

🟧 Mettre un decorateur sur l'API gateway ?

🟧 Encoder les clefs SSL de NGINX ?

🟧 Mettre un bouton retour HOME sur les pages d'erreur (maxi casse couilles)

🟧 Avoir les pages d'erreurs 404/500 sur `login/` et `regsiter/`

🟧 ADMIN DOIT RESTER ID 1

🟧 Disable SwaggerUI in `docs_url=None,`  ===>  `main.py` 

🟧 LIMITER LA LENGHT DES INPUTS DANS LES FORMULAIRES



======================================= DONE =====================================


✅ XSS

✅ Injection SQL sur tout les formulaires

✅ UUID, le slash a la fin urls.py (si on met le slash, tout pete)

✅ Create a worklofo to delete the DB at 42

✅ Test and stabilize multi-users connection (once everything is locked up) 


--------------------------------------------------------------------------------
									XSS /SQL
--------------------------------------------------------------------------------

# XSS





# Injection SQL

"SELECT * FROM users WHERE username = '$username' AND password = '$password'";


✅
username: ' OR '1'='1
password: anything

✅
username: admin' --
password: anything

✅
username: ' UNION SELECT null, 'hacked', null --
password: anything

✅
username: ' OR IF(1=1, SLEEP(5), 0) --
password: anything






--------------------------------------------------------------------------------
									DB
--------------------------------------------------------------------------------


```python

import requests

url = 'http://databaseapi:8007/api/match/'
data = {
    'player1': 5,
    'player2': 3,
    'winner': 3,
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())

```



```python

import requests

url = 'http://databaseapi:8007/api/tournament/'

response = requests.get(url)
print(response.status_code)
print(response.json())

```

Extract the last ID in python

```python

data = [{'id': 1, 'winner_tournament': 11}, {'id': 2, 'winner_tournament': 13}]
last_id = data[-1]['id']
print(last_id)  # Output: 2


```

--------------------------------------------------------------------------------
									TOUDOU
--------------------------------------------------------------------------------


✅ TODO FOR DELETING THE DATABASE

✅ METTRE LES CHAMPS REQUIRED DANS DELETE-PROFILE.HTMl sur les champs password et otp

✅ Tester le multi login sur la branche `prevent_double_auth`

✅ TESTER LE WORKLOW : Register -> turn on 2FA -> Logout -> Login -> 2FA -> Disable 2fa -> Logout -> Login -> delete user -> Login

✅ CREER DES TEST AVEC LE CSRF TOKEN	

✅ FIX LES TEST DES 2FA QUI PLANTES PARFOIS dans playright


`STABILIZATION`:

## BASE REQUIREMENTS

✅ Bouton Back and Forward (notaament dans un match)
✅ Pong contre soi-meme
✅ Tournoi 
✅ Mettre des alias a chaque debut de tournoi
🟧 Injections SQL / XSS
✅ HTTPS (wss)
🟧 Secure routes API


⛔ ✅  
## DONE OF THE DAY
✅  Simplifies the django admin panel credentials 


## TO DO LATER
⛔ ✅  Split `admin` id from the `Players` logic to avoid getting disconnected (complicated, if we can avoid it is good )

⛔ ✅ La route `http://localhost:8000/login/` fonctionne, mais la route `http://localhost:8000/login` (check ngninx or fastAPI shit) 


# PRIORITY

⛔ ✅  Strip every useless requirements logics from `user`, `authentication` and `database-api`


## JWT :

✅ Create a very specific login and register route free of JWT requirements
⛔ ✅ Transfert the ping logic from a `curl` command to let the `auth` container handle the logic
⛔ ✅
⛔ ✅
⛔ ✅

⛔ ✅ Connect the form for login in the first place WITHOUT 2FA
⛔ ✅ Create a first version of a JWT.
⛔ ✅ Then displays the token on the front with a redirection


⛔ ✅  Possibly leverage django filters


⛔ ✅ centraliser la documentation django / database / container

--------------------------------------------------------------------------------
									DATABASE ENDPOINTS
--------------------------------------------------------------------------------

```python

INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',  # This must be BEFORE CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    ...
]

# CORS CONFIGURATION
CORS_ALLOW_CREDENTIALS = True  # 🔥 Allow cookies in requests
CORS_ALLOW_ORIGINS = [
    "http://localhost:8000",  # Basic
    "http://localhost:8001",  # Tournament
    "http://localhost:8002",  # Match
    "http://localhost:8003",  # Static files
    "http://localhost:8004",  # User
    "http://localhost:8005",  # FastAPI
    "http://localhost:8006",  # Authentication
    "http://localhost:8007",  # DatabaseAPI
    f"https://{HOST_IP}",  # Production
]
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
CORS_ALLOW_HEADERS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
CORS_ALLOW_HEADERS = ["*"]


--------------------------------------------------------------------------------
									TO ASK
--------------------------------------------------------------------------------


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
✅  Optimize `entrypoint.sh` for  `database_api`
✅  Start making endpoints

📅  ===== 18-03 =====


✅ Create a user `two_fa_app` django_app

✅ Make a route with simple HTML rendering with SPA

✅ SetUp 2FA => Render QR Code + Validation
✅ Once validated the timestamp code => Write in models the key

✅ Then check within the models if data has been correctly wrote

✅ Turn the SetUp2FA button is the user has not enable

✅ Create Disable 2FA is the user has it enabled