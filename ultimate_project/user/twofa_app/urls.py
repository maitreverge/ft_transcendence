from django.urls import path
from . import views

urlpatterns = [
    path("setup-2fa/", views.setup_2fa, name="setup_2fa"),
    path("verify-2fa/", views.verify_2fa, name="verify_2fa"),
]
