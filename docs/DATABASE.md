# TRANSCENDENCE DATABASES :

The databases are stored in the container `postgres`, short for PostgreSQL.

There is also a bind-mount on it (it is stored locally at `/home/volumes_transcendence/postgres`)

Sometimes, after merges, data might be corrupted in your database because of massive changes.

To start fresh, run

```bash
./migrations_delete.sh
```

> [!NOTE]
> This commands just deletes migrations changes which will be applied in your database
> This does not delete actual data, but rather the way data is structured within the database.

```bash
make delete_volume
```
is also a solution for deleting your database. This action can't be undone.


# HOW DO I ACCESS THE DATABASE :

Go at the following URL :
http://localhost:8000/admin/

This is the Django Admin Pannel. It's a premade built-in solution from Django for visualizing data.

DJANGO-ADMIN CREDENTIALS :

### LOGIN
admin@example.com

### PASSWORD
adminpassword


Once in the panel, you can access the models under the `User_Management_App` section.

> [!WARNING]
> Do not modify ANY data under the others sections.


## HOW TO CREATE MODELS.

A Django model is a Python class that defines a database table.

Each model:

- Maps to a table in PostgreSQL.
- Defines fields (columns) and their data types.
- Provides an API for querying and modifying data.


```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Player(AbstractBaseUser):
    """
    Represents a Player in the system.
    - Managed by the `user` service.
    - Stored in `user_schema.player` table in PostgreSQL.
    """

    # 🔹 Primary Key (Unique ID for each player)
    id = models.AutoField(primary_key=True)

    # 🔹 Authentication Fields
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    # 🔹 Personal Information
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=True)

    # 🔹 Account Status
    is_active = models.BooleanField(default=True)

    # 🔹 Django Authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        managed = True  # ✅ This model is managed by the `user` service
        db_table = "player"  # ✅ PostgreSQL will store this in `user_schema.player`

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

```

> [!CAUTION]
> The models are managed EXCLUSIVELLY by the `user_app_management` in the `user` container scope.

## I WANT TO MODIFY A MODEL :

### STEP ONE :

Modify the models in `ultimate_project/user/user_management_app/models.py`.

Your model MUST obey to the following structure :

```python
class ModelName(models.Model):
    # 1️⃣ Database Fields (Attributes)
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()
    
    # 2️⃣ Django-Specific Constants (ALL_CAPS)
    REQUIRED_FIELDS = ["field1"]
    USERNAME_FIELD = "field2"

    # 3️⃣ Meta Class (For Model Configuration)
    class Meta:
        db_table = "table_name"
        managed = True

    # 4️⃣ Dunder (Magic) Methods (e.g., __str__, __repr__)
    def __str__(self):
        return self.field1

    # 5️⃣ Custom Model Methods (Any additional logic)
    def custom_method(self):
        return self.field2 * 2
```

### STEP TWO :

Reflects the changes made in the following files :
- `ultimate_project/match/match_app/models.py`.
- `ultimate_project/tournament/tournament_app/models.py`.

> [!CAUTION]
> THERE IS TWO MAJOR DIFFERENCES BETWEEN MODELS in 
> `ultimate_project/user/user_management_app/models.py`
> and the two others files you'll copy your changes


#### DIFFERENCE ONE:

The original model at `ultimate_project/user/user_management_app/models.py`will most of the time inherit from a Django base model like.

```python
class Tournament(models.Model):
```

The models implemented in others places will inherit from the `CrossSchemaModel`. Everytime.

```python
class Tournament(CrossSchemaModel):
```

#### DIFFERENCE TWO:

The Meta Subclass (which manages the models in Django gears) is also different
In `ultimate_project/user/user_management_app/models.py`

The meta class looks like this :

```python
    class Meta:
        managed = True # This indicates that the `user` service is managing it in the Postgres DB.
        db_table = "tournament"
```

whereas in others places

```python
    class Meta:
        managed = False # This indicates that the current service DO NOT MANAGE the model.
        db_table = "tournament"
```



## ADDITIONAL WORKSPACES COMMANDS

`make rebuilt` ==> Delete every containers

## TROUBLESHOOTING

Sometimes, when switching branches, you can have old migrations which you can't delete.

You need to 

```
sudo chown -R $USER:$USER .
```
at the root of transendence project.

