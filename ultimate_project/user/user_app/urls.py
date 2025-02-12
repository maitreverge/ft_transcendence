# USER USER_APP

from django.urls import path

from .import views

urlpatterns = [
    path("", views.test),
    path("login", views.login)
]