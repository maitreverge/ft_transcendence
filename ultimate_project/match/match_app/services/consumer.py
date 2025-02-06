from channels.generic.websocket import AsyncWebsocketConsumer
import json
import sys
import logging

logger = logging.getLogger(__name__)


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Accepte la connexion websocket

    async def disconnect(self, close_code):
        pass  # Actions à réaliser lors de la déconnexion

    async def receive(self, text_data):
        # data = json.loads(text_data)  # Décode le message JSON reçu
        data = json.loads(text_data)
        print(
            f"ici houston, voila l'action {data.get('action')}, \
                et puis voila la direction {data.get('direction')}\n"
        )

        sys.stdout.flush()
        logger.info("🚀 loggerinfo !")
        await self.send(
            text_data=json.dumps(
                f"from server ici houston, \
                                 on a recu ça {text_data}"
            )
        )  # Envoie une réponse
