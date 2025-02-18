from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="auth_index"),
    path("login/", views.login_view, name="login"),
    path("signin/", views.signin_view, name="signin"),
    path("logout/", views.logout_view, name="logout"),
]   
