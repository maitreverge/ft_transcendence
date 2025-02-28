from django.contrib import admin
from django.urls import path, include

from . import views
from . import two_fa

urlpatterns = [
    path("", views.index, name="auth_index"),
    path("login/", views.login_view, name="login"),
    path("signin/", views.signin_view, name="signin"),
    path("logout/", views.logout_view, name="logout"),
    path("logout/", views.logout_view, name="logout"),
    path("enable_2fa/", two_fa.enable_2fa, name="enable_2fa"),
]   
