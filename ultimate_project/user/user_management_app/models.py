from django.db import models
from django.contrib.auth.models import AbstractBaseUser


#  ================= MODELS MANAGED BY THIS MICROSERVICE (user) =================
class Player(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Tells Django to use "email" as the primary field for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        managed = (
            True  # This service is responsible for creating and managing this model
        )
        db_table = "player"  # Explicitly set the schema and table name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = "tournament"

    def __str__(self):
        return f"Tournament {self.id}"


class Match(models.Model):
    id = models.AutoField(primary_key=True)

    player1 = models.ForeignKey(
        to=Player,  # Explicit reference to Player model
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

    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.SET_NULL,  # If the tournament is deleted, set this field to NULL
        null=True,
        blank=True,
    )

    class Meta:
        managed = True
        db_table = "match"

    def __str__(self):
        return f"Match {self.id}"
