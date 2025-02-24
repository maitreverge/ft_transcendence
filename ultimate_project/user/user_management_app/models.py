from django.db import models

# Create your models here.
class UserManagementDummyModel(models.Model):
    name = models.CharField(max_length=100)
    name_dummy = models.CharField(max_length=100)
    name_dummy_2 = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'user_schema.usermanagementdummymodel'
    
    def __str__(self):
        return self.name