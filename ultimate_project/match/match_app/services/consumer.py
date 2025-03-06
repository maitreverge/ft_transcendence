from channels.generic.websocket import AsyncWebsocketConsumer
import json
import urllib
from match_app.views import pongs

players = []

class MyConsumer(AsyncWebsocketConsumer):

	async def connect(self):

		self.matchId = self.scope["url_route"]["kwargs"]["matchId"]    
		query_string = self.scope["query_string"].decode() 	
		params = urllib.parse.parse_qs(query_string)
		self.playerId = int(params.get("playerId", [None])[0])
		match = next((p for p in pongs if p.id ==  self.matchId), None)
		await self.accept()
		if match is None:
			await self.close(code=3000)
			return
		players.append({
			'playerId': self.playerId,
			'matchId': self.matchId,
			'socket': self,
			'dir': None
		})
		await self.send({'newPlayer': self.playerId})	

	async def disconnect(self, close_code):
		global players
		players[:] = [p for p in players if p['socket'] != self]
		
	async def receive(self, text_data):		
		data = json.loads(text_data)	
		for p in players: 
			if p['socket'] == self:
				p['dir'] = data.get('dir')
