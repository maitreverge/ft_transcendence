from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PlayerViewSet, TournamentViewSet, MatchViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'player', PlayerViewSet)
router.register(r'tournament', TournamentViewSet)
router.register(r'match', MatchViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]