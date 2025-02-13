# USER USER_APP

from django.urls import path

from . import views
from . import login

app_name = "login"

urlpatterns = [
    path("", views.test, name="index"),
    path("signin", login.sign_in, name="sign_in"),
    path("add", login.add, name="add"),
]