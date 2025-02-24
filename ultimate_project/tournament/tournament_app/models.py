from django.db import models

# Create your models here.
class TournamentDummyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'tournament_schema.tournamentdummymodel'
    
    def __str__(self):
        return self.name