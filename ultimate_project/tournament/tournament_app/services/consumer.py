from channels.generic.websocket import AsyncWebsocketConsumer
import json
import requests
import aiohttp

players = []
selfPlayers = []
matchs = []

class MyConsumer(AsyncWebsocketConsumer):

	id = 0
	async def connect(self):				
		await self.accept() 
		MyConsumer.id += 1
		self.id = MyConsumer.id
		players.append({'playerId': self.id, 'busy': False})
		selfPlayers.append({'playerId': self.id, 'socket': self})
		await self.send(text_data=json.dumps({
			"type": "selfAssign", "selfId": self.id})) 
		for selfplay in selfPlayers:
			await selfplay['socket'].send(text_data=json.dumps({
				"type": "playerList",
				"players": players
			}))
			await selfplay['socket'].send(text_data=json.dumps({
				"type": "matchList",
	 			"matchs": matchs
			}))

	async def disconnect(self, close_code):
		global selfPlayers
		global players				
		selfPlayers[:] = [p for p in selfPlayers if p['socket'] != self]
		players[:] = [p for p in players if p['playerId'] != self.id]
		for selfplay in selfPlayers:
			await selfplay['socket'].send(text_data=json.dumps({
				"type": "playerList",
				"players": players
			}))		

	@staticmethod
	async def match_update():
		for selfplay in selfPlayers:
			await selfplay['socket'].send(text_data=json.dumps({
				"type": "matchList",
				"matchs": matchs
			}))

	async def cancel_invitation(self,
		applicantPlayer, selectedPlayer, selfSelectedPlayer, selectedId):

		if applicantPlayer \
			and applicantPlayer.get('busy') \
			and applicantPlayer.get('pair') \
			and applicantPlayer.get('pair') == selectedPlayer:
			await self.send(text_data=json.dumps({
				"type": "invitation",
				"subtype": "cancel",
				"targetId": selectedId,				
			}))
			await selfSelectedPlayer['socket'].send(text_data=json.dumps({
				"type": "invitation",
				"subtype": "cancel",
				"targetId": self.id,				
			}))
			selectedPlayer['busy'] = None				
			selectedPlayer['pair'] = None
			applicantPlayer['busy'] = None
			applicantPlayer['pair'] = None
			match = next((m for m in matchs if self.id in (m.get('playerId'), m.get('otherId'))))
			await self.stop_match(self.id, match.get('matchId'))						
			return True
		return False
	
	async def invitation(self, selectedId):

		selectedPlayer = next(
			(p for p in players if p['playerId'] == selectedId), None)
		selfSelectedPlayer = next(
			(p for p in selfPlayers if p['playerId'] == selectedId), None)	
		applicantPlayer = next(
			(p for p in players if p['playerId'] == self.id), None)

		if await self.cancel_invitation(
			applicantPlayer, selectedPlayer, selfSelectedPlayer, selectedId):		
			return

		if applicantPlayer and applicantPlayer.get('busy'):
			await self.send(text_data=json.dumps({
				"type": "invitation",
				"subtype": "back",
				"applicantId": self.id,
				"response": "selfBusy"
			}))
			return			
		for p in selfPlayers:
			if p['playerId'] == selectedId:
				if selectedPlayer.get('busy'):
					await self.send(text_data=json.dumps({
						"type": "invitation",
						"subtype": "back",
						"applicantId": self.id,
						"response": "selectedBusy"
					}))
					break			
				await p['socket'].send(text_data=json.dumps({
					"type": "invitation",
					"subtype": "demand",
					"applicantId": self.id
				}))			
				selectedPlayer['busy'] = True				
				selectedPlayer['pair'] = applicantPlayer
				applicantPlayer['busy'] = True
				applicantPlayer['pair'] = selectedPlayer

	async def start_match(self, applicantId):

		match_id = requests.get(
			f"http://match:8002/match/new-match/?p1={applicantId}&p2={self.id}"
		).json()['matchId']
		matchs.append({
			"matchId": match_id,
			"playerId": applicantId, 
			"otherId": self.id
		})
		return match_id		

	async def stop_match(self, applicant_id, match_id):

		url = f"http://match:8002/match/stop-match/{applicant_id}/{match_id}/"

		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				status = response.status
				data = await response.json()		
		if response.status == 200:			
			matchs[:] = [m for m in matchs
				if m.get("matchId") != str(match_id)]			
			await MyConsumer.match_update()
			
	async def confirmation(self, response, applicantId):

		match_id = None
		selfApplicantPlayer = next(
			(p for p in selfPlayers if p['playerId'] == applicantId), None)

		if response:
			match_id = await self.start_match(applicantId)

		data = {
			"type": "invitation",
			"subtype": "confirmation",
			"response": response,
			"applicantId": applicantId,
			"selectedId": self.id,
			"matchId": match_id			
		}
		await selfApplicantPlayer['socket'].send(text_data=json.dumps(data))
		await self.send(text_data=json.dumps(data))
		await MyConsumer.match_update()

	async def receive(self, text_data):		
		data = json.loads(text_data)
		match data:
			case {"type": "playerClick", "selectedId": selectedId}:
				await self.invitation(selectedId)				

			# case {"type": "invitation"}:
			# 	for p in selfPlayers:
			# 		if p['playerId'] == data['selectedId']:
			# 			await p['socket'].send(text_data=json.dumps({
			# 				"type": "invitation",
			# 				"playerId": self.id
			# 			}))
			# case {"type": "cancelInvitation"}:
			# 	for p in selfPlayers:
			# 		if p['playerId'] == data['selectedId']:
			# 			await p['socket'].send(text_data=json.dumps({
			# 				"type": "cancelInvitation",
			# 				"playerId": self.id
			# 			}))
			case {"type": "confirmation", "response": response, "applicantId": applicantId}:
				await self.confirmation(response, applicantId)
				# for p in selfPlayers:
				# 	if p['playerId'] == data['applicantId']:
				# 		await p['socket'].send(text_data=json.dumps({
				# 			"type": "confirmation",
				# 			"response": response,
				# 			"selectedId": self.id
				# 		}))
			case _ if data.get("matchId") is not None:		
				for p in selfPlayers:
					if p['playerId'] == data['selectedId']:
						await p['socket'].send(text_data=json.dumps({
							"matchId": data['matchId']
						}))
			case _:
				pass  
