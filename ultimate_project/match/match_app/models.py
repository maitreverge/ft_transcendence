from django.db import models

# Create your models here.
class MatchDummyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'match_schema.matchdummymodel'

    def __str__(self):
        return self.name