from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login-form/", views.login_form, name="login-form"),
    path("login/", views.login, name="login"),
    path("tournament/", views.tournament, name="tournament"),
    path("simple-match/", views.simple_match, name="simple-match"),
    path("home/", views.home),
]
