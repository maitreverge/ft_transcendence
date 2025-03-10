import json
import requests
import asyncio

class Tournament():
	
	id = 0
	def __init__(self, applicantId):

		Tournament.id += 1
		self.id = Tournament.id
		self.players = []
		self.matchs = []
		self.n_match = 0

	async def append_player(self, player):
		self.players.append(player)
		if len(self.players) >= 4:
			for player in self.players:				
				await player.send(text_data=json.dumps({
					"type": "getPattern",
					"tournamentId": self.id					
				}))
			await asyncio.sleep(3)#//!
			await self.launchTournament()	
				
	def remove_player(self, player):
		self.players[:] = [p for p in self.players if p != player]

	async def launchTournament(self):
		await self.start_match(self.players[0].id, self.players[1].id, "m2")
		await self.start_match(self.players[2].id, self.players[3].id, "m3")

	async def start_match(self, p1, p2, local_match_id):
		match_id = requests.get(
			f"http://match:8002/match/new-match/?p1={p1}&p2={p2}"
		).json().get('matchId', None)
		if match_id:
		# 	print(f"MATCHID FROM TOURNOISS {match_id}, p1 {p1}, p2 {p2}", flush=True)
			self.matchs.append({"matchId": match_id})		
			for player in self.players:				
				await player.send(text_data=json.dumps({
					"type": "linkMatch",
					"localMatchId": local_match_id,			
					"matchId": match_id,
				}))			
	
	async def match_result(self, match_id, winner_id, looser_id):
		print(f"winner is {winner_id}, and looser is {looser_id}", flush=True)
		self.n_match += 1
		match = next(
			(m for m in self.matchs if m.get('matchId') == match_id)	
		, None)
		if match:
			match['winnerId'] = winner_id
			match['looserId'] = looser_id
		if self.n_match == 2:
			await self.start_match(
				self.matchs[0].get('winnerId'), self.matchs[1].get('winnerId'), "m1")

					