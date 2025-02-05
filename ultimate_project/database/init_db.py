from django.db import models

# TODO : Implement 1 class == 1 table with Django ORM Models
class User(models.Model):
    username = models.CharField
    # password
    # email
    # ect...

class Match(models.Model):