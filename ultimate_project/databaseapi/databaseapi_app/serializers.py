from rest_framework import serializers
from .models import Player, Tournament, Match, PlayerStatistics

""" 
🔄 Convert Django model instances (like your PlayerStatistics) to 
JSON — so they can be sent over an API.

📥 Validate and deserialize incoming JSON from requests — 
so it can be saved to the database. """


class PlayerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Player
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "two_fa_enabled",
            "_two_fa_secret",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Extract password from validated data
        password = validated_data.pop("password", None)

        # Create user instance without saving to database
        user = Player(**validated_data)

        # If password was provided, set it using the set_password method
        if password:
            user.set_password(password)

        # Save the user
        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password updates separately
        password = validated_data.pop("password", None)

        # Update all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If password was provided, hash it
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class PlayerNestedSerializer(serializers.ModelSerializer):
    """A simplified serializer for nesting within other serializers"""

    class Meta:
        model = Player
        fields = ["username", "first_name", "last_name"]


class PlayerStatisticsSerializer(serializers.ModelSerializer):
    stats_history = serializers.JSONField(required=False)
    class Meta:
        model = PlayerStatistics
        fields = [
            "player",
            "games_played",
            "games_won",
            "games_lost",
            "points_scored",
            "points_conceded",
            "win_rate",
            "average_score",
            "best_win_streak",
            "c_win_streak",
            "worst_lose_streak",
            "c_lose_streak",
            "nb_tournaments_played",
    		"nb_tournaments_won",
            "last_updated",
            "stats_history", #lifetime daily stat history
        ]


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = [
            "id",
            "winner_tournament",
        ]


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
            "score_p1",
            "score_p2",
        ]
