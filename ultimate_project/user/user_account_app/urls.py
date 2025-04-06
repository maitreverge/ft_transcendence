from django.urls import path, include
# from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async, async_to_sync
# from django.views.decorators.http import require_http_methods, require_POST, require_GET

from .views.profile import profile_view
from .views.game_stats import game_stats_view
from .views.security import security_view
from .views.security.twofa import twofa_views
from .views.confidentiality import conf_view
#from .views.confidentiality.delete_account import delete_view

from django.urls import path

urlpatterns = [
    # Profile page
    path("profile/", profile_view.profile_view, name="profile"),
    # Game stats page
    path("game-stats/", game_stats_view.game_stats_view, name="game-stats"),
    # Security page
    path("security/", security_view.security_view, name="security-main-page"),
    path("security/verify-2fa/", twofa_views.verify_2fa_view, name="verify-2fa"),
    path("security/setup-2fa/", twofa_views.setup_2fa_view, name="setup-2fa"),
    path("security/disable-2fa/", twofa_views.disable_2fa_view, name="disable-2fa"),
    # Confidentiality page
    path("confidentiality/", conf_view.conf_view, name="conf-main-page"),
    #path("confidentiality/delete-account/", delete_view.delete_profile_view, name="delete-account"),
]
