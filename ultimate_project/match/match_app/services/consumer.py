from channels.generic.websocket import AsyncWebsocketConsumer
import json
import urllib
from match_app.views import pongs
import aiohttp
import asyncio

players = []

class MyConsumer(AsyncWebsocketConsumer):

	async def connect(self):

		self.matchId = self.scope["url_route"]["kwargs"]["matchId"]    
		query_string = self.scope["query_string"].decode() 	
		params = urllib.parse.parse_qs(query_string)
		self.playerId = int(params.get("playerId", [None])[0])
		print(f"CONNECT plyid {self.playerId} matchid {self.matchId}", flush=True)
		match = next((p for p in pongs if p.id ==  self.matchId), None)
		await self.accept()
		if match is None:
			print(f"MATCH NONE id {self.playerId}", flush=True)
			await self.close(code=3000)
			return
		player = next(
			(p for p in players if p.get('playerId') == self.playerId)
			, None)
		if player:
			print(f"PLAYER YET EXIST selfid {self.playerId} pid {player.playerId}", flush=True)
			await self.close(code=3000)
			return
		players.append({
			'playerId': self.playerId,
			'matchId': self.matchId,
			'socket': self,
			'dir': None
		})
		await self.send_players_update()	

	async def disconnect(self, close_code):
		print(f"DISCONNECTE selid {self.playerId} matchid {self.matchId}", flush=True)
		global players
		players[:] = [p for p in players if p['socket'] != self]
		await asyncio.sleep(1)
		await self.send_players_update()

	async def receive(self, text_data):				
		data = json.loads(text_data)	
		for p in players: 
			if p['socket'] == self:
				p['dir'] = data.get('dir')

	async def send_players_update(self):
	
		async with aiohttp.ClientSession() as session:
			async with session.post(
				"http://tournament:8001/tournament/match-players-update/",
				json={
				"matchId": self.matchId,
				"players": [{
					key : value for key, value in p.items() if key == 'playerId'
					} for p in players if p.get('matchId') == self.matchId				
				]}) as resp:
					if resp.status != 200 and resp.status != 201:
						err = await resp.text()
						print(f"Error HTTP {resp.status}: {err}", flush=True)
