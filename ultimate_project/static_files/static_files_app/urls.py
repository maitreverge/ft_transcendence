from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login-form/", views.login_form, name="login-form"),
    path("login/", views.login, name="login"),
    path("home/", views.home),
    path("user/profil/", views.profil),
    path("user/stats/", views.stats),
]
