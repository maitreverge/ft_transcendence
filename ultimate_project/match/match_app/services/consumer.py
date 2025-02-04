from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Accepte la connexion websocket

    async def disconnect(self, close_code):
        pass  # Actions à réaliser lors de la déconnexion

    async def receive(self, text_data):
        data = json.loads(text_data)  # Décode le message JSON reçu
        await self.send(text_data=json.dumps({"message": "Réponse du serveur"}))  # Envoie une réponse
