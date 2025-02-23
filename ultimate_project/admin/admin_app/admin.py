from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AuthDummyModel, UserManagementDymmyModel, TournamentDummyModel, MatchDummyModel

admin.site.register(AuthDummyModel)
admin.site.register(UserManagementDymmyModel)
admin.site.register(TournamentDummyModel)
admin.site.register(MatchDummyModel)
# admin.site.register()
