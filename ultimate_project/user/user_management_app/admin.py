from django.contrib import admin
from .models import Player, Tournament, Match


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "player1", "player2", "winner", "tournament")
