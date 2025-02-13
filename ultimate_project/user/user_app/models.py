from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


# USER TABLE
# class User(models.Model):
#     username = models.CharField(
#         max_length=42,
#         unique=True,
#         validators=[
#             MinLengthValidator(5, "the field must contain at least 5 characters")
#         ],
#     )
#     password = models.CharField(
#         max_length=30,
#         validators=[
#             MinLengthValidator(5, "the field must contain at least 5 characters")
#         ],
#     )
#     age = models.PositiveIntegerField()

#     def __str__():
#         return f"User : {self.username}\nHashed Password = {self.password}\nAge: {self.age}"
