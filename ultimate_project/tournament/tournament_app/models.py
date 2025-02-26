from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# This is an abstract base model that other models can inherit from.
# It does NOT create a table in the database but allows us to share common behavior.
class CrossSchemaModel(models.Model):
    
    class Meta:
        abstract = True  # This ensures Django does not create a table for this model.


#  ================= MODEL MANAGED BY THIS MICROSERVICE (user) =================
class Player(CrossSchemaModel):
    # Unique ID for each player
    id = models.AutoField(primary_key=True)

    # User authentication fields
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True)

    # Personal details
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=True)

    # Active status of the user
    is_active = models.BooleanField(default=True)

    # Tells Django to use "email" as the primary field for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # ✅ Ensures username is still required

    class Meta:
        managed = False  # This service is responsible for creating and managing this model
        db_table = "player"  # Explicitly set the schema and table name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


#  ================= MODEL MANAGED BY OTHER MICROSERVICES =================
class Tournament(CrossSchemaModel):
    # Unique ID for each tournament
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False  # This microservice does NOT manage this model (tournament microservice does)
        db_table = "tournament"  # Explicitly set the schema and table name

    def __str__(self):
        return f"Tournament {self.id}"


class Match(CrossSchemaModel):
    id = models.AutoField(primary_key=True)

    player1 = models.ForeignKey(
        to=Player,  # Explicit reference to Player model in the `user` app
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
        related_name="winner",  # Allows querying Match objects where this player was the winner
    )

    tournament = models.ForeignKey(
        to=Tournament,  # Explicit reference to Tournament model from tournament service
        on_delete=models.SET_NULL,  # If the tournament is deleted, set this field to NULL
        null=True,
        blank=True,
    )

    class Meta:
        managed = False  # This microservice does NOT manage this model (match microservice does)
        db_table = "match"  # Explicitly set the schema and table name

    def __str__(self):
        return f"Match {self.id}"