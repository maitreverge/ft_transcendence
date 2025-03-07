from rest_framework import viewsets
from .models import Player, Tournament, Match
from .serializers import PlayerSerializer, TournamentSerializer, MatchSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing players (read-only)
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TournamentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing tournaments (read-only)
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing matches (read-only)
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer