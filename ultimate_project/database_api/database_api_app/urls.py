from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PlayerViewSet, TournamentViewSet, MatchViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'tournaments', TournamentViewSet)
router.register(r'matches', MatchViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]