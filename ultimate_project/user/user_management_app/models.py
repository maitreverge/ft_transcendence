from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Player(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    class Meta:
        # managed = False
        db_table = 'user_schema.player'
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Match(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'match_schema.match'


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'tournament_schema.tournament'