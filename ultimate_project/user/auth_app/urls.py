from django.urls import path

from . import views
from . import two_fa

urlpatterns = [
    path("", views.index, name="auth_index"),
    path("login/", views.login_view, name="login"),
    path("signin/", views.signin_view, name="signin"),
    path("logout/", views.logout_view, name="logout"),
    path("logout/", views.logout_view, name="logout"),
    path("setup_2fa/", two_fa.setup_2fa, name="setup_2fa"),
]
