✅
⛔
🟧
⚠️
--------------------------------------------------------------------------------
									DUMP IDEAS
--------------------------------------------------------------------------------

DATABASE MIGRATIONS :
⛔ ✅  

# PRIORITY
✅  Create a database_api service

## MODELS
✅  Move the managed models in this one
✅  Delete all the others models
✅  Simplify the models ( maybe already simplified )


## COMPOSE // DOCKER
✅  Remove the healthchecks for old containers
✅  Create the service database_api
✅  Remove the postgres clients from others containers


## SETTINGS
✅  Roll back to dummy config like

```python
DATABASES = {}
```
✅  Remove Admin apps in `INSTALLED_APPS`
✅  Remove Database MiddleWares
✅  Remove anything Database Related
⛔ ✅  
✅  Simplify the SQL schemas to have none


⛔ ✅  Split `admin` id from the `Players` logic to avoid getting disconnected
⛔ ✅  Strip every cipher / encryption logic into the `database_api` container



⛔ ✅  Move the `django-admin` managing logic to the 
⛔ ✅  Possibly leverage django filters


```python
# default database stuff
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```


⛔ ✅ centraliser la documentation django / database / container


--------------------------------------------------------------------------------
									MY ROUTES
--------------------------------------------------------------------------------
http://localhost:8000/admin/  ==>  ADMIN PANEL


http://localhost:8000/user/
http://localhost:8000/auth/  ==>  redirect to http://localhost:8000/auth/login/





--------------------------------------------------------------------------------
									DATABASE
--------------------------------------------------------------------------------

```python

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),  # Name of the Database
        "USER": os.getenv("POSTGRES_USER"),  # Username for accessing the database
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # Password for the database user.
        "HOST": os.getenv(
            "POSTGRES_HOST"
        ),  # Hostname where the database server is running == compose service == Name of the db
        "PORT": os.getenv(
            "POSTGRES_PORT"
        ),  # Port number on which the database server is listening.
        "OPTIONS": {
            "options": "-c search_path=user_schema"
        },
    }
}

```


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
















```python
# OLD MODELS

from django.db import models


# This is an abstract base model that other models can inherit from.
# It does NOT create a table in the database but allows us to share common behavior.
class CrossSchemaModel(models.Model):

    class Meta:
        abstract = True  # This ensures Django does not create a table for this model.


#  ================= MODELS MANAGED BY OTHER MICROSERVICES =================
class Player(CrossSchemaModel):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, blank=True)

    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 2FA fields
    two_fa_enabled = models.BooleanField(default=False)
    two_fa_verified = models.BooleanField(default=False)
    _two_fa_secret = models.CharField(
        max_length=32, blank=True, null=True
    )  # ✅ Store 2FA secret

    # Tells Django to use "email" as the primary field for authentication
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        managed = False
        db_table = "player"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tournament(CrossSchemaModel):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "tournament"

    def __str__(self):
        return f"Tournament {self.id}"


class Match(CrossSchemaModel):
    id = models.AutoField(primary_key=True)

    player1 = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="player1",
    )
    player2 = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="player2",
    )
    winner = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="winner",
    )

    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "match"

    def __str__(self):
        return f"Match {self.id}"


```