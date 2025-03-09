from channels.generic.websocket import AsyncWebsocketConsumer
import json
from tournament_app.services.tournament import Tournament
from typing import List

players : List["TournamentConsumer"] = []
tournaments : List["Tournament"] = []

class TournamentConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		await self.accept()
		self.id = int(self.scope["url_route"]["kwargs"]["user_id"])
		players.append(self)
		await self.send(text_data=json.dumps({
			"type": "selfAssign", "selfId": self.id})) 
		await self.send_all("player", players)
		await self.send_tournaments()

	async def disconnect(self, close_code):
		players[:] = [p for p  in players if p.id != self.id]
		await self.send_all("player", players)

	# async def send_players(self):		
	# 	for player in players:
	# 		await player.send(text_data=json.dumps({
	# 			"type": "playerList",			
	# 			"players": [
	# 				{"playerId": p.id} for p in players
	# 			]
	# 		}))

	# async def send_tournaments(self):		
	# 	for player in players:
	# 		await player.send(text_data=json.dumps({
	# 			"type": "tournamentList",			
	# 			"tournaments": [
	# 				{"tournamentId": t.id} for t in tournaments
	# 			]
	# 		}))

	async def send_tournaments(self):	
		print(f"SEND TOURNAMENT", flush=True)	
		for player in players:
			await player.send(text_data=json.dumps({
				"type": "tournamentList",			
				"tournaments": [
					{"tournamentId": t.id, "players":
	   		[{"playerId": p.id} for p in t.players]
	   } for t in tournaments
				]
			}))

	async def send_all(self, message_type, source):		
		for player in players:
			await player.send(text_data=json.dumps({
				"type": message_type + "List",			
				message_type + "s": [
					{message_type + "Id": s.id} for s in source
				]
			}))

	async def receive(self, text_data):
		print(f"receive!", flush=True)
		data = json.loads(text_data)
		match data:
			case {"type": "newTournament"}:
				await self.new_tournament()
			case {"type": "enterTournament", "tournamentId": tournament_id}:
				print(f"case entertournament!", flush=True)
				await self.enter_tournament(tournament_id)		
			case _:
				pass

	async def new_tournament(self):	
		tournaments.append(Tournament(self.id))
		await self.send_tournaments()

	async def enter_tournament(self, tournament_id):
		print(f"entertournement : {tournament_id}", flush=True)

		for t in tournaments:
			print(t.id, flush=True)
			if t.id == tournament_id:			
				t.append(self)
				await self.send_tournaments()
		