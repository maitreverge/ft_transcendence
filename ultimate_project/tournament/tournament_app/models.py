from django.db import models


class CrossSchemaModel(models.Model):
    """
    This is an abstract base model that other models can inherit from.
    It does NOT create a table in the database but allows us to share common behavior.
    """

    class Meta:
        abstract = True  # This ensures Django does not create a table for this model.


#  ================= MODEL MANAGED BY THIS MICROSERVICE (match) =================
class Tournament(models.Model):
    # Unique ID for each tournament
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = (
            "tournament_schema.tournament"  # Explicitly set the schema and table name
        )

    def __str__(self):
        return f"Tournament {self.id}"


#  ================= MODEL MANAGED BY OTHER MICROSERVICES =================
class Player(CrossSchemaModel):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    class Meta:
        managed = False  # ! This microservice does NOT manage this model (user microservice does)
        db_table = "user_schema.player"  # Explicitly set the schema and table name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Match(CrossSchemaModel):
    # Unique ID for each match
    id = models.AutoField(primary_key=True)

    # ForeignKeys referencing Player (users)
    player1 = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,  # If a player is deleted, the match is also deleted
        related_name="player1",  # Allows querying Match objects where the player was player1
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

    # ForeignKey to Tournament
    tournament = models.ForeignKey(
        to=Tournament,  # Explicit reference to Tournament model from tournament service
        on_delete=models.SET_NULL,  # If the tournament is deleted, set this field to NULL
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "match_schema.match"

    def __str__(self):
        return f"Match {self.id}"


#  ================= MODEL MANAGED BY OTHER MICROSERVICES =================
