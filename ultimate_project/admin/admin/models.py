# admin/models.py
from django.db import models

class AuthDummyModel(models.Model):
    name = models.CharField(max_length=100)
    name_dummy = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_schema.authdummymodel'
    
    def __str__(self):
        return self.name

class UserManagementDummyModel(models.Model):
    name = models.CharField(max_length=100)
    name_dummy = models.CharField(max_length=100)
    name_dummy_2 = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_schema.usermanagementdummymodel'
    
    def __str__(self):
        return self.name
    
class MatchDummyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'match_schema.matchdummymodel'

    def __str__(self):
        return self.name

class TournamentDummyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'tournament_schema.tournamentdummymodel'
    
    def __str__(self):
        return self.name
    
