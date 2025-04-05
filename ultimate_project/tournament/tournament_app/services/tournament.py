import json
import requests
import asyncio
import aiohttp

class Tournament():
	
	id = 0
	def __init__(self, applicantId):
		
		Tournament.id += 1
		self.id = Tournament.id
		self.launch = False
		self.players = []
		self.matchs = []
		self.n_match = 0

	async def append_player(self, player):

		self.players.append(player)
		if len(self.players) >= 4 and not self.launch:	
			await self.launchTournament()	
				
	async def remove_player(self, player):

		print(f"REMOVE PLAYER {player.id}", flush=True)
		self.players[:] = [p for p in self.players if p != player]
		if not self.players:	
			await self.del_tournament()

	async def del_tournament(self):

		print(f"DEL TOURNAMENT {self.id}", flush=True)
		from tournament_app.services.tournament_consumer \
			import tournaments, TournamentConsumer
		tournaments[:] = [t for t in tournaments if t.id != self.id]
		await TournamentConsumer.send_tournaments()

	async def launchTournament(self):

		self.launch = True
		p1 = (self.players[0].id, self.players[0].name)
		p2 = (self.players[1].id, self.players[1].name)
		p3 = (self.players[2].id, self.players[2].name)
		p4 = (self.players[3].id, self.players[3].name)
		await self.start_match(p1, p2, "m2")
		await self.start_match(p3, p4, "m3")

	async def start_match(self, p1, p2, local_match_id):

		print(f"START MATCH p1:{p1[0]} {p1[1]} p2:{p2[0]} {p2[1]} lmt:{local_match_id}", flush=True)
		async with aiohttp.ClientSession() as session:
			async with session.get(				
    				f"http://match:8002/match/new-match/"
					f"?p1Id={p1[0]}&p1Name={p1[1]}&p2Id={p2[0]}&p2Name={p2[1]}"
				) as response:
				if response.status == 201:
					data = await response.json()
					match_id = data.get('matchId', None)					
					link_match = {
						"type": "linkMatch",
						"tournamentId": self.id,
						"localMatchId": local_match_id,			
						"matchId": match_id,
						"p1Id": p1[0], "p2Id": p2[0],
						"p1Name": p1[1], "p2Name": p2[1],
					}
					match = {
						"matchId": match_id,						
						"linkMatch": link_match
					}
					self.matchs.append(match)
					print(f"FIN STARTMATCH {link_match}", flush=True)
					return link_match
				else:  
					err = await response.text()
					print(f"Error HTTP {response.status}: {err}", flush=True)


	# async def match_result(self, data):

	# 	match_id = data.get('matchId')
	# 	winner_id = data.get('winnerId')
	# 	looser_id = data.get('looserId')
	# 	winner_name = data.get('winnerName')
	# 	looser_name = data.get('looserName')
	# 	score = data.get('score')
	# 	p1_id = data.get('p1Id')
	# 	p2_id = data.get('p2Id')
	# 	print(f"winner is {winner_id}, and looser is {looser_id}", flush=True)

	# 	# winner = next((p for p in self.players if p.id == winner_id), None)
	# 	# looser = next((p for p in self.players if p.id == looser_id), None)	
	# 	self.n_match += 1
	# 	match = next(
	# 		(m for m in self.matchs if m.get('matchId') == match_id), None)
	# 	if match:
	# 		match_result = {				
	# 			"type": "matchResult",
	# 			"tournamentId": self.id,
	# 			"localMatchId": match.get('linkMatch', {}).get('localMatchId'),			
	# 			"matchId": match_id,
	# 			"p1Id": p1_id,
	# 			"p2Id": p2_id,
	# 			"winnerId": winner_id,
	# 			"looserId": looser_id,
	# 			"winnerName": winner_name,
	# 			"looserName": looser_name,
	# 			"score": score			
	# 		}
	# 		match['matchResult'] = match_result
	# 		match['matchPlayersUpdate'] = None
	# 	await self.workflow(match_result)
	
	async def match_result(self, data):

		match_id = data.get('matchId')		
		self.n_match += 1
		match = next(
			(m for m in self.matchs if m.get('matchId') == match_id), None)
		if match:
			match_result = {				
				"type": "matchResult",
				"tournamentId": self.id,
				"localMatchId": match.get('linkMatch', {}).get('localMatchId'),			
				**data			
			}
			match['matchResult'] = match_result
			match['matchPlayersUpdate'] = None
		await self.workflow(match_result)

	async def workflow(self, match_result):

		if self.n_match == 1:
			await self.send_match_result(match_result)
		elif self.n_match == 2:
			# p1 = (self.matchs[0].get('matchResult', {}).get('winnerId'),
			# 	self.matchs[0].get('matchResult', {}).get('winnerName'))
			# p2 = (self.matchs[1].get('matchResult', {}).get('winnerId'),
			# 	self.matchs[1].get('matchResult', {}).get('winnerName'))
			nxt_plys = self.get_next_players()
			link_match = await self.start_match(nxt_plys[0], nxt_plys[1], "m1")			
			await self.send_match_result(match_result)
			await self.send_link_match(link_match)
		elif self.n_match == 3:
			await self.send_match_result(match_result)
			tournament_result = self.get_tournament_result(match_result)
			await self.send_tournament_result(tournament_result)
			self.launch = False

	def get_next_players(self):

		return (
			(
				self.matchs[0].get('matchResult', {}).get('winnerId'),
				self.matchs[0].get('matchResult', {}).get('winnerName')
			),	
			(
				self.matchs[1].get('matchResult', {}).get('winnerId'),
				self.matchs[1].get('matchResult', {}).get('winnerName')
			)
		)
		
	def get_tournament_result(self, match_result):

		return {
			"tournamentId": self.id,
			"winner_id": match_result.get('winnerId'),
			"winner_name": match_result.get('winnerName'),
			"looser_id": match_result.get('looserId'),
			"looser_name": match_result.get('looserName'),
			"matchs": self.matchs
		}

	async def send_tournament_result(self, tournament_result):
		print(f"SENDLINKMATCH {tournament_result}", flush=True)	
		from tournament_app.services.tournament_consumer import players
		for player in players:
			print(f"SENDLINKMATCH {tournament_result} to {player.id}", flush=True)				
			await player.send(text_data=json.dumps(tournament_result))

	async def send_link_match(self, link_match):

		print(f"SENDLINKMATCH {link_match}", flush=True)	
		from tournament_app.services.tournament_consumer import players
		for player in players:
			print(f"SENDLINKMATCH {link_match} to {player.id}", flush=True)				
			await player.send(text_data=json.dumps(link_match))

	async def send_match_result(self, match_result):

		print(f"SENDMATCHRESULT {match_result}", flush=True)
		from tournament_app.services.tournament_consumer import players
		for player in players:
			print(f"SENDMATCHRESULT {match_result} to {player.id}", flush=True)					
			await player.send(text_data=json.dumps(match_result))

	async def match_players_update(self, match_update):

		print(f"MATCH PLAYERS UPDATE {match_update}", flush=True)
		match = next(
			(m for m in self.matchs
			if m.get('matchId') == match_update.get('matchId'))
		, None)
		if match:
			match_update['type'] = 'matchPlayersUpdate'
			match_update['tournamentId'] = self.id
			match_update['localMatchId'] = match.get('linkMatch', {}).get(
				'localMatchId')
			match_update['p1Id'] = match.get('linkMatch', {}).get('p1Id')
			match_update['p2Id'] = match.get('linkMatch', {}).get('p2Id')
			match['matchPlayersUpdate'] = match_update
			await self.send_match_players_update()

	async def send_match_players_update(self):	

		from tournament_app.services.tournament_consumer \
			import TournamentConsumer
		await TournamentConsumer.send_matchs_players_update()
					