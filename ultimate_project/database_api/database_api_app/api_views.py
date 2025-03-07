from rest_framework import viewsets
from .models import Player, Tournament, Match
from .serializers import PlayerSerializer, TournamentSerializer, MatchSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing players
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing tournaments
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing matches
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer