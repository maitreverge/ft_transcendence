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

	async def receive(self, text_data):		
		data = json.loads(text_data)
		match data:
			case {"type": "playerClick", "selectedId": selectedId}:
				await self.invitation(selectedId)				
			case {
				"type": "confirmation",
				"response": response,
				"applicantId": applicantId
			}:
				await self.confirmation(response, applicantId)		
			case _:
				pass
			
	async def invitation(self, selectedId):

		selectedPlayer = next(
			(p for p in players if p['playerId'] == selectedId), None)
		selfSelectedPlayer = next(
			(p for p in selfPlayers if p['playerId'] == selectedId), None)	
		applicantPlayer = next(
			(p for p in players if p['playerId'] == self.id), None)
		applicantPlayer = next(
			(p for p in players if p['playerId'] == self.id), None)
		if await self.cancel_invitation(
			applicantPlayer, selectedPlayer, selfSelectedPlayer, selectedId):		
			return
		if applicantPlayer and applicantPlayer.get('busy'):
			await self.send_back("selfBusy")
			return
		if selectedPlayer and selectedPlayer.get('busy'):
			await self.send_back("selectedBusy")
			return	
		await self.send_demand(
			selfSelectedPlayer, selectedPlayer,	applicantPlayer
		)
		
	async def send_back(self, response):		
		await self.send(text_data=json.dumps({
			"type": "invitation",
			"subtype": "back",
			"applicantId": self.id,
			"response": response
		}))
		
	async def cancel_invitation(self,
		applicantPlayer, selectedPlayer, selfSelectedPlayer, selectedId):

		if applicantPlayer \
			and applicantPlayer.get('busy') \
			and applicantPlayer.get('busy') == selectedId:
			await self.send_cancel(selectedId, self)		
			await self.send_cancel(self.id, selfSelectedPlayer['socket'])		
			selectedPlayer['busy'], applicantPlayer['busy'] = None, None					
			match = next(
				(m for m in matchs 
	 				if self.id in (m.get('playerId'), m.get('otherId'))),
				None)
			if match:
				await self.stop_match(self.id, match.get('matchId'))						
			return True
		return False

	async def send_cancel(self, targetId, target):		
		await target.send(text_data=json.dumps({
			"type": "invitation",
			"subtype": "cancel",
			"targetId": targetId,			
		}))
		
	async def send_demand(self, 
		selfSelectedPlayer, selectedPlayer, applicantPlayer):

		await selfSelectedPlayer['socket'].send(text_data=json.dumps({
			"type": "invitation",
			"subtype": "demand",
			"applicantId": self.id
		}))				
		selectedPlayer['busy'] = applicantPlayer.get('playerId')
		applicantPlayer['busy'] = selectedPlayer.get('playerId')
			
	async def confirmation(self, response, applicantId):
		print(f"confirmation applicant: {applicantId}", flush=True)
		match_id = None
		selfApplicantPlayer = next(
			(p for p in selfPlayers if p['playerId'] == applicantId), None)
		selected_player = next(
			(p for p in players if p['playerId'] == self.id), None)
		applicant_player = next(
			(p for p in players if p['playerId'] == applicantId), None)
		if response:
			if applicant_player and applicant_player.get('busy') and applicant_player.get('busy') == self.id:
				match_id = await self.start_match(applicantId)
			else:
				print(f"ANNULED", flush=True)
				return
			# if applicant_player \
			# and applicant_player.get('busy') \
			# and applicant_player.get('busy') == self.id:
		elif applicant_player and applicant_player.get('busy') and applicant_player.get('busy') == self.id:
			applicant_player['busy'], selected_player['busy'] = None, None			
		else:
			return	
		await self.send_confirmation_back(
			response, applicantId, self.id, match_id,
			selfApplicantPlayer['socket']
		)
		await self.send_confirmation_back(
			response, applicantId, applicantId, match_id, self
		)
		await MyConsumer.match_update()

	async def send_confirmation_back(self,
		response, applicant_id, target_id, match_id, target):
		await target.send(text_data=json.dumps({
			"type": "invitation",
			"subtype": "confirmation",
			"response": response,
			"applicantId": applicant_id,
			"targetId": target_id,			
			"matchId": match_id	
		}))

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

	@staticmethod
	async def match_update():
		for selfplay in selfPlayers:
			await selfplay['socket'].send(text_data=json.dumps({
				"type": "matchList",
				"matchs": matchs
			}))
