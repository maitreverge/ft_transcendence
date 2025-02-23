from django.db import models

# ==================  USER  ==================
class AuthDummyModel(models.Model):
    name = models.CharField(max_length=100)
    name_dummy = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserManagementDymmyModel(models.Model):
    name = models.CharField(max_length=100)
    name_dummy = models.CharField(max_length=100)
    name_dummy_2 = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# ==================  TOURNAMENT  ==================

class TournamentDummyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# ==================  MATCH  ==================
class MatchDummyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name