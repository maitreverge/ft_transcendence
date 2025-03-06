from django.urls import path
from tournament_app.services.consumer import MyConsumer 

websocket_urlpatterns = [
    path(
        "ws/tournament/<str:user_id>/", MyConsumer.as_asgi()
    ),
]
