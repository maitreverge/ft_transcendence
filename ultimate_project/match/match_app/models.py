from django.db import models


# This is an abstract base model that other models can inherit from.
# It does NOT create a table in the database but allows us to share common behavior.
class CrossSchemaModel(models.Model):

    class Meta:
        abstract = True  # This ensures Django does not create a table for this model.


#  ================= MODELS MANAGED BY OTHER MICROSERVICES =================
class Player(CrossSchemaModel):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, blank=True)

    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 2FA fields
    two_fa_enabled = models.BooleanField(default=False)
    two_fa_verified = models.BooleanField(default=False)
    _two_fa_secret = models.CharField(
        max_length=32, blank=True, null=True
    )  # ✅ Store 2FA secret

    # Tells Django to use "email" as the primary field for authentication
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        managed = False
        db_table = "player"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tournament(CrossSchemaModel):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "tournament"

    def __str__(self):
        return f"Tournament {self.id}"


class Match(CrossSchemaModel):
    id = models.AutoField(primary_key=True)

    player1 = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="player1",
    )
    player2 = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="player2",
    )
    winner = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="winner",
    )

    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "match"

    def __str__(self):
        return f"Match {self.id}"
