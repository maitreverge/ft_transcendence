from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.http import Http404
from django_filters import rest_framework as filters
from django.utils import timezone
from rest_framework.response import Response
from .models import Player, Tournament, Match, PlayerStatistics
from .serializers import PlayerSerializer, TournamentSerializer, MatchSerializer, PlayerStatisticsSerializer
from datetime import datetime, timedelta
import time

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

class PlayerStatisticsFilter(filters.FilterSet):
    # use the id of the player model using the '__' to acess the id
    player = filters.CharFilter(field_name='player__id', lookup_expr='icontains')  # Filter by player's username

    class Meta:
        model = PlayerStatistics
        fields = ['player_id']

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
                {"error": "Player object not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class PlayerStatisticsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStatistics.objects.all()
    serializer_class = PlayerStatisticsSerializer
    filterset_class = PlayerStatisticsFilter

    @action(detail=True, methods=['POST'], url_path='update-stats')
    def update_stats(self, request, player_id=None):
        try:
            # Get the player statistics by player_id
            player_stats, created = PlayerStatistics.objects.get_or_create(player=player_id)
            print(f"Printing player stats for player_id {player_id} info: {player_stats}", flush=True)
            #debug to rm
            if created:
                print("New stats created for player w id :", player_id)
            else:
                print("Existing stats found for player w id:", player_id)
            
            data = {
                "games_played": 1,  
                "games_won": 1 if request.data.get("winner") == player_id else 0,
                "games_lost": 1 if request.data.get("winner") != player_id else 0,
                "points_scored": request.data.get('points_scored', 0),
                "points_conceded": request.data.get('points_conceded', 0),
            }
            player_stats.games_played += data["games_played"]
            player_stats.games_won += data["games_won"]
            player_stats.games_lost += data["games_lost"]
            player_stats.points_scored += data["points_scored"]
            player_stats.points_conceded += data["points_conceded"]
            update_record = {
                "games_played": data["games_played"],
                "games_won": data["games_won"],
                "games_lost": data["games_lost"],
                "points_scored": data["points_scored"],
                "points_conceded": data["points_conceded"],
            }
            now = timezone.localtime(timezone.now())
            today_str = now.date().isoformat()
            print(f"\nTODAY STR {today_str}\n\n", flush=True) #rm
            if today_str in player_stats.update_history:
                existing_record = player_stats.update_history[today_str]
                existing_record["games_played"] += data["games_played"]
                existing_record["games_won"] += data["games_won"]
                existing_record["games_lost"] += data["games_lost"]
                existing_record["points_scored"] += data["points_scored"]
                existing_record["points_conceded"] += data["points_conceded"]
            else:
                player_stats.update_history[today_str] = update_record
            # Max 30 days history for game stats per day
            thirty_days_ago = timezone.now() - timedelta(days=30)
            filtered_history = {}
            for key_str, value in player_stats.update_history.items():
                key_date = datetime.fromisoformat(key_str).date()
                if key_date >= thirty_days_ago.date():
                    filtered_history[key_str] = value
            player_stats.update_history.clear()
            player_stats.update_history = filtered_history
            player_stats.save()
            return Response({
                "message": "Player stats updated successfully",
                "stats": PlayerStatisticsSerializer(player_stats).data
            }, status=status.HTTP_200_OK)
        except PlayerStatistics.DoesNotExist:
            return Response({
                "error": "Player statistics not found"
            }, status=status.HTTP_404_NOT_FOUND)

    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response(
                {"error": "Player statistics not found"}, 
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