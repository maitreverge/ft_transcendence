from django.urls import path
from match_app.services.consumer import MyConsumer

websocket_urlpatterns = [
    path(
        "ws/match/<int:matchId>/", MyConsumer.as_asgi()
    ),
]
