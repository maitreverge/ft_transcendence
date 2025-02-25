from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class Player(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    class Meta:
        # managed = False
        db_table = "user_schema.player"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    player1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player1"
    )
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player2"
    )
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="winner")
    tournament = models.ForeignKey(
        "Tournament", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        managed = False
        db_table = "match_schema.match"

    def __str__(self):
        pass


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "tournament_schema.tournament"

    def __str__(self):
        return f"Tournament {self.id}"
