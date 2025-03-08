from channels.generic.websocket import AsyncWebsocketConsumer
import json
from typing import List

players : List["TournamentConsumer"] = []

class TournamentConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		await self.accept()
		self.id = int(self.scope["url_route"]["kwargs"]["user_id"])
		players.append(self)
		await self.send(text_data=json.dumps({
			"type": "selfAssign", "selfId": self.id})) 
		await self.send_players()

	async def disconnect(self, close_code):
		players[:] = [p for p  in players if p.id != self.id]
		await self.send_players()

	async def send_players(self):		
		for player in players:
			await player.send(text_data=json.dumps({
				"type": "playerList",			
				"players": [
					{"playerId": p.id} for p in players
				]
			}))