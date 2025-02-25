from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# This is an abstract base model that other models can inherit from.
# It does NOT create a table in the database but allows us to share common behavior.
class CrossSchemaModel(models.Model):
    
    class Meta:
        abstract = True  # This ensures Django does not create a table for this model.


#  ================= MODEL MANAGED BY THIS MICROSERVICE (user) =================
class Player(AbstractBaseUser):
    """
    The Player model represents a user in the system.
    - This model is fully managed by the `user` microservice.
    - It is stored in the `user_schema` schema in the PostgreSQL database.
    """
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

    class Meta:
        managed = True  # This service is responsible for creating and managing this model
        db_table = "user_schema.player"  # Explicitly set the schema and table name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


#  ================= MODEL MANAGED BY OTHER MICROSERVICES =================
class Match(CrossSchemaModel):
    """
    This is a representation of the `Match` model from the `match` microservice.
    
    - The `Match` microservice manages this model, NOT the `user` microservice.
    - We include it here only for Django ORM compatibility (ForeignKey relationships).
    - This model is set to `managed = False`, so Django does NOT create/migrate this table.
    """

    id = models.AutoField(primary_key=True)

    player1 = models.ForeignKey(
        to="user_management_app.Player",  # Explicit reference to Player model in the `user` app
        on_delete=models.CASCADE,  # If a player is deleted, the match is also deleted
        related_name="player1",  # Allows querying Match objects where the player was player1
    )
    player2 = models.ForeignKey(
        to="user_management_app.Player",
        on_delete=models.CASCADE,
        related_name="player2",
    )
    winner = models.ForeignKey(
        to="user_management_app.Player",
        on_delete=models.CASCADE,
        related_name="winner",  # Allows querying Match objects where this player was the winner
    )

    tournament = models.ForeignKey(
        to="tournament_app.Tournament",  # Explicit reference to Tournament model from tournament service
        on_delete=models.SET_NULL,  # If the tournament is deleted, set this field to NULL
        null=True,
        blank=True,
    )

    class Meta:
        managed = False  # This microservice does NOT manage this model (match microservice does)
        db_table = "match_schema.match"  # Explicitly set the schema and table name

    def __str__(self):
        return f"Match {self.id}"


#  ================= MODEL MANAGED BY OTHER MICROSERVICES =================
class Tournament(CrossSchemaModel):
    """
    This is a representation of the `Tournament` model from the `tournament` microservice.
    
    - The `Tournament` microservice manages this model, NOT the `user` microservice.
    - We include it here only for Django ORM compatibility (ForeignKey relationships).
    - This model is set to `managed = False`, so Django does NOT create/migrate this table.
    """

    # Unique ID for each tournament
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False  # This microservice does NOT manage this model (tournament microservice does)
        db_table = "tournament_schema.tournament"  # Explicitly set the schema and table name

    def __str__(self):
        return f"Tournament {self.id}"
