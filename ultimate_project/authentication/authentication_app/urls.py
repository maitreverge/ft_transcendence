from django.urls import path

from . import views
# from . import two_fa

urlpatterns = [
    # path("", views.index, name="auth_index"),
    path("login/", views.login_view, name="login"),
]
