from channels.generic.websocket import AsyncWebsocketConsumer
import json
import urllib
from match_app.views import pongs
import requests

players = []

class MyConsumer(AsyncWebsocketConsumer):

	async def connect(self):

		self.matchId = self.scope["url_route"]["kwargs"]["matchId"]    
		query_string = self.scope["query_string"].decode() 	
		params = urllib.parse.parse_qs(query_string)
		self.playerId = int(params.get("playerId", [None])[0])
		print(f"HOULALA matchid {self.matchId} playereid: {self.playerId}", flush=True)
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
		self.send_players_update()	

	async def disconnect(self, close_code):
		global players
		players[:] = [p for p in players if p['socket'] != self]
		self.send_players_update()

	async def receive(self, text_data):				
		data = json.loads(text_data)	
		for p in players: 
			if p['socket'] == self:
				p['dir'] = data.get('dir')

	def send_players_update(self):
		requests.post(
		"http://tournament:8001/tournament/match-players-update/", json={
			"matchId": self.matchId,
			"players": [
				{key : value for key, value in p.items() if key == 'playerId'}
				for p in players if p.get('matchId') == self.matchId
			]
		})
