# USER USER_APP

from django.urls import path

from . import views
from . import oauth2

urlpatterns = [
    path("", views.test),
    path("login", oauth2.oauth_42)
]