import json
import requests
import asyncio
import aiohttp

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
			await self.send_get_pattern()
			await asyncio.sleep(3)#//!
			await self.launchTournament()	
				
	def remove_player(self, player):
		self.players[:] = [p for p in self.players if p != player]

	async def send_get_pattern(self):
		for player in self.players:				
			await player.send(text_data=json.dumps({
				"type": "getPattern",
				"tournamentId": self.id					
			}))

	async def launchTournament(self):
		await self.start_match(self.players[0].id, self.players[1].id, "m2")
		await self.start_match(self.players[2].id, self.players[3].id, "m3")

	async def start_match(self, p1_id, p2_id, local_match_id):
	
		async with aiohttp.ClientSession() as session:
			async with session.get(				
    				f"http://match:8002/match/new-match/?p1={p1_id}&p2={p2_id}"
				) as response:
				if response.status == 201:
					data = await response.json()
					match_id = data.get('matchId', None)					
					link_match = {
						"type": "linkMatch",
						"tournamentId": self.id,
						"localMatchId": local_match_id,			
						"matchId": match_id,
						"p1Id": p1_id,
						"p2Id": p2_id
					}
					match = {
						"matchId": match_id,						
						"linkMatch": link_match
					}
					self.matchs.append(match)
					return link_match
					# await self.send_link_match(link_match)
		
	async def send_link_match(self, link_match):
		from tournament_app.services.tournament_consumer import players
		for player in players:				
			await player.send(text_data=json.dumps(link_match))

	# async def send_match_update()
	async def match_result(self, match_id, winner_id, looser_id):
		print(f"winner is {winner_id}, and looser is {looser_id}", flush=True)
		self.n_match += 1
		match = next(
			(m for m in self.matchs if m.get('matchId') == match_id)	
		, None)
		if match:
			# match['winnerId'] = winner_id
			# match['looserId'] = looser_id
			match_result = {				
				"type": "matchResult",
				"tournamentId": self.id,
				"localMatchId": match.get('linkMatch', {}).get('localMatchId'),			
				"matchId": match_id,
				"p1Id": match.get('linkMatch', {}).get('p1Id'),
				"p2Id": match.get('linkMatch', {}).get('p2Id'),
				"winnerId": winner_id,
				"looserId": looser_id			
			}
			match['matchResult'] = match_result
		print(self.matchs, flush=True)
		if self.n_match == 1:
			await self.send_match_result(match_result)
		if self.n_match == 2:
			link_match = await self.start_match(
				self.matchs[0].get('matchResult', {}).get('winnerId'),
				self.matchs[1].get('matchResult', {}).get('winnerId'),				  
				"m1")			
			await self.send_match_result(match_result)
			await self.send_link_match(link_match)
		elif self.n_match == 3:
			print(f"THE FINAL WINNER IS :{winner_id}", flush=True)
			await self.send_match_result(match_result)

	async def send_match_result(self, match_result):
		from tournament_app.services.tournament_consumer import players
		for player in players:				
			await player.send(text_data=json.dumps(match_result))

	async def match_players_update(self, match_update):
		print(f"MATCH PLAYERS UPDATE {match_update}", flush=True)
		match = next(
			(m for m in self.matchs if m.get('matchId') == match_update.get('matchId'))	
		, None)
		if match:
			match_update['type'] = 'matchPlayersUpdate'
			match_update['tournamentId'] = self.id
			match_update['localMatchId'] = match.get('linkMatch', {}).get(
				'localMatchId')
			match_update['p1Id'] = match.get('linkMatch', {}).get('p1Id'),
			match_update['p2Id'] = match.get('linkMatch', {}).get('p2Id'),
			match['matchPlayersUpdate'] = match_update
			await self.send_match_players_update(match_update)

	async def send_match_players_update(self, match_update):		
		from tournament_app.services.tournament_consumer import players
		for player in players:				
			await player.send(text_data=json.dumps(match_update))
					