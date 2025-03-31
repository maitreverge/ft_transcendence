from django.urls import path
from tournament_app.services.simple_match_consumer import SimpleConsumer 
from tournament_app.services.tournament_consumer import TournamentConsumer

websocket_urlpatterns = [
    path(
		"ws/tournament/simple-match/<int:user_id>/<str:user_name>/",
		SimpleConsumer.as_asgi()),
    path(
		"ws/tournament/tournament/<int:user_id>/<str:user_name>/",
		TournamentConsumer.as_asgi())
]
