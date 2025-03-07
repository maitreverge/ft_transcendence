from rest_framework import serializers
from .models import Player, Tournament, Match


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "username", "email", "first_name", "last_name"]


class PlayerNestedSerializer(serializers.ModelSerializer):
    """A simplified serializer for nesting within other serializers"""

    class Meta:
        model = Player
        fields = ["username", "first_name", "last_name"]


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ["id"]


class MatchSerializer(serializers.ModelSerializer):
    # Add nested player data
    player1_details = PlayerNestedSerializer(source="player1", read_only=True)
    player2_details = PlayerNestedSerializer(source="player2", read_only=True)
    winner_details = PlayerNestedSerializer(source="winner", read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "player1",
            "player1_details",
            "player2",
            "player2_details",
            "winner",
            "winner_details",
            "tournament",
        ]
