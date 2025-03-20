from rest_framework import serializers
from .models import Player, Tournament, Match


class PlayerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    profile_picture_url = serializers.SerializerMethodField(read_only=True)

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
            "profile_picture",
            "profile_picture_url",
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

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None


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
