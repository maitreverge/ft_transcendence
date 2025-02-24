from django.contrib import admin
from .models import AuthDummyModel, UserManagementDummyModel, MatchDummyModel, TournamentDummyModel

# Register your models here.
admin.site.register(AuthDummyModel)
admin.site.register(UserManagementDummyModel)
admin.site.register(MatchDummyModel)
admin.site.register(TournamentDummyModel)
