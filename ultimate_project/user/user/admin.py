from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_management_app.models import Player, Tournament, Match


class PlayerAdmin(admin.ModelAdmin):
    pass

class TournamentAdmin(admin.ModelAdmin):
    pass

class MatchAdmin(admin.ModelAdmin):
    pass

admin.site.register(Player, PlayerAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)