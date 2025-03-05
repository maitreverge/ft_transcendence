from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login-form/", views.login_form, name="login-form"),
    path("login/", views.login, name="login"),
    path("home/", views.home),
    path("user/profile/", views.profile),
    path("user/stats/", views.stats),
    path("tournament-match-wrapper/", views.match_simple_template, name="tournament_match_wrapper"),
]
