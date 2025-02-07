from channels.generic.websocket import AsyncWebsocketConsumer
import json
import sys
import logging

logger = logging.getLogger(__name__)

players = []

class MyConsumer(AsyncWebsocketConsumer):

	async def connect(self):        
		await self.accept() 
		id = len(players) + 1
		players.append({'id': id, 'socket': self})

	async def disconnect(self, close_code):
		global players
		players = [p for p in players if p['socket'] != self]
		pass

	async def receive(self, text_data):
		
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
