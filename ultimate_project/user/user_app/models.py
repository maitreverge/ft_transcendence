from django.db import models
from django.core.validators import MinLengthValidator


# USER TABLE
class User(models.Model):
    username = models.CharField(
        max_length=42,
        unique=True,
        validators=[
            MinLengthValidator(5, "the field must contain at least 5 characters")
        ],
    )
    password = models. # TODO
    age = models.PositiveIntegerField(min=18, max=120)


    def __str__():
        return f"User : {self.username}\n"
