from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("home/", views.home),
    path("user/profile/", views.profile),
    path("user/stats/", views.stats),
    path(
        "tournament-match-wrapper/<str:user_id>/",
        views.match_simple_template,
        name="tournament_match_wrapper",
    ),
    path(
        "tournament-wrapper/<str:user_id>/",
        views.tournament_template,
        name="tournament_wrapper",
    ),
    path(
        "user-profile-wrapper/",
        views.user_profile_template,
        name="user_profile_template",
    ),
    path("user-stats-wrapper/", views.user_stats_template, name="user_stats_template"),
    path("translations/<str:lang>.json", views.translations, name="translations"),
    path("register/", views.register, name="register"),
    path("forgot-password/", views.forgotPassword, name="forgot-password"),
    path("login/", views.forgotPassword, name="login"),
    path("auth2f/", views.twoFactorAuth, name="login"),
    path("error/<int:code>/", views.error, name="error"),
]
