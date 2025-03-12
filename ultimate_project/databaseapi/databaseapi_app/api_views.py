from rest_framework import viewsets, status
from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework.response import Response
from .models import Player, Tournament, Match
from .serializers import PlayerSerializer, TournamentSerializer, MatchSerializer

# ====================================== FILTERS =======================================
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

# ====================================== VIEWS SETS ====================================
class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing players
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response(
                {"error": "Player not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class TournamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing tournaments (read-only)
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response(
                {"error": "Player not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing matches (read-only)
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filterset_class = MatchFilter

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response(
                {"error": "Player not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )