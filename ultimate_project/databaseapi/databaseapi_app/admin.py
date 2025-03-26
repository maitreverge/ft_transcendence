from django.contrib import admin
from .models import Player, Tournament, Match


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "is_active")
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("email",)

    # Ensure passwords are hashed when saving a Player in the admin.
    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:  # Only hash if password was changed
            obj.set_password(obj.password)  # Hash the password before saving
        super().save_model(request, obj, form, change)


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "player1", "player2", "winner", "tournament")
