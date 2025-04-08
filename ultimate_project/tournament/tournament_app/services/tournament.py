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
			await self.send_all_players(match_result)
		elif self.n_match == 2:		
			nxt_plys = self.get_next_players()
			link_match = await self.start_match(nxt_plys[0], nxt_plys[1], "m1")			
			await self.send_all_players(match_result)
			await self.send_all_players(link_match)
		elif self.n_match == 3:
			await self.send_all_players(match_result)
			tournament_result = self.get_tournament_result(match_result)
			await self.send_all_players(tournament_result)
			await self.send_db(tournament_result)
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
			"type": "tournamentResult",
			"tournamentId": self.id,
			"winnerId": match_result.get('winnerId'),
			"winnerName": match_result.get('winnerName'),
			"looserId": match_result.get('looserId'),
			"looserName": match_result.get('looserName'),
			"matchs": self.matchs
		}

	async def send_all_players(self, packet):

		from tournament_app.services.tournament_consumer \
			import TournamentConsumer
		await TournamentConsumer.send_all_players(packet)

    # ! ================ SEND DB =================
	async def save_tournament_matches(self, matches, tournament_id):
		
		from tournament_app.views import send_db as update_match

		path = "api/match/"
		
		for _ in range(3):
			
			# Extract each key individually
			tournament = tournament_id
			p1 = max(1, matches[_]["matchResult"]["p1Id"])
			p2 = max(1, matches[_]["matchResult"]["p2Id"])
			win = max(1, matches[_]["matchResult"]["winnerId"])
			score_p1 = matches[_]["matchResult"]["score"][0]
			score_p2 = matches[_]["matchResult"]["score"][1]
			
			# Compile each key in a JSON body
			data = {
				"player1": p1,
				"player2": p2,
				"winner": win,
				"score_p1": score_p1,
				"score_p2": score_p2,
				"tournament": tournament,
			}
			await update_match(path, data)

	async def extract_last_tournament_id(self):
		
		async with aiohttp.ClientSession() as session:
			async with session.get(
				f"http://databaseapi:8007/api/tournament/") as response:				
				if response.status not in (200, 201):
					full_response = response.json()
					return full_response[-1]["id"] # [-1] access the last block of json


	async def send_db(self, tournament_result):

		from tournament_app.views import send_db as sdb

		path = "api/tournament/"
		
		winner = tournament_result["winnerId"]
		
		data_tournament = {
			"winner_tournament" : winner,
		}
		await sdb(path, data_tournament)

		# Need to extract the last tournament update
		id_tournament = self.extract_last_tournament()
		
		await self.save_tournament_matches(tournament_result["matchs"], id_tournament)
		
		
		
    # ! ================ SEND DB =================

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
					