from django.urls import path
from tournament_app.services.simple_match_consumer import SimpleConsumer 
from tournament_app.services.tournament_consumer import TournamentConsumer

websocket_urlpatterns = [
    path("ws/tournament/<str:user_id>/", SimpleConsumer.as_asgi()),
    path(
		"ws/tournament/tournament/<int:user_id>/", TournamentConsumer.as_asgi())
]
