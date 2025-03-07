from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import Player, Tournament, Match
from .serializers import PlayerSerializer, TournamentSerializer, MatchSerializer

# Define filter sets for each model
class PlayerFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Player
        fields = ['username', 'email']

class MatchFilter(filters.FilterSet):
    player1 = filters.NumberFilter()
    player2 = filters.NumberFilter()
    tournament = filters.NumberFilter()
    
    class Meta:
        model = Match
        fields = ['player1', 'player2', 'tournament']

class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing players (read-only)
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter

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
    filterset_class = MatchFilter