"""
URL configuration for tournament project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path
import tournament_app.views
from django.http import HttpResponse

# Compose health-check, do not remove
def health_check(request):
    return HttpResponse(status=200)

urlpatterns = [
    path('health/', health_check, name='health_check'), # Compose health-check, do not remove
    path("tournament/", tournament_app.views.start_tournament),
    path("test/", tournament_app.views.test),
]
