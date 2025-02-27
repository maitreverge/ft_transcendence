from channels.generic.websocket import AsyncWebsocketConsumer
import json

players = []
selfPlayers = []
matchs = []

class MyConsumer(AsyncWebsocketConsumer):

	id = 0
	async def connect(self):				
		await self.accept() 
		MyConsumer.id += 1
		self.id = MyConsumer.id
		players.append({'playerId': self.id})
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

	async def receive(self, text_data):		
		data = json.loads(text_data)
		match data:			
			case {"type": "invitation"}:
				for p in selfPlayers:
					if p['playerId'] == data['selectedId']:
						await p['socket'].send(text_data=json.dumps({
							"type": "invitation",
							"playerId": self.id
						}))
			case {"type": "cancelInvitation"}:
				for p in selfPlayers:
					if p['playerId'] == data['selectedId']:
						await p['socket'].send(text_data=json.dumps({
							"type": "cancelInvitation",
							"playerId": self.id
						}))
			case {"type": "confirmation", "response": response, **rest}:
				for p in selfPlayers:
					if p['playerId'] == data['applicantId']:
						await p['socket'].send(text_data=json.dumps({
							"type": "confirmation",
							"response": response,
							"selectedId": self.id
						}))
			case _ if data.get("matchId") is not None:		
				for p in selfPlayers:
					if p['playerId'] == data['selectedId']:
						await p['socket'].send(text_data=json.dumps({
							"matchId": data['matchId']
						}))
			case _:
				pass  
