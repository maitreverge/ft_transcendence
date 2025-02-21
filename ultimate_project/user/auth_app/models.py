from django.db import models

# Create your models here.
class UserDummyModelAuth(models.Model):
    name = models.CharField(max_length=100)
    name_dummy = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name