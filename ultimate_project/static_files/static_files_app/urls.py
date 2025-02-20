from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login-form/", views.login_form, name="login-form"),
    path("login/", views.login, name="login"),
    path("simple-match/", views.simple_match, name="simple-match"),
    path('translations/<str:lang>.json', views.translations, name='translations'),
]
