from rest_framework import serializers
from .models import Player, Tournament, Match


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        # Note: We're omitting password and security fields for basic API


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'player1', 'player2', 'winner', 'tournament']