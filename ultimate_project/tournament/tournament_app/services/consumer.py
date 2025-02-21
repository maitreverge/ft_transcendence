from channels.generic.websocket import AsyncWebsocketConsumer
import json

players = []
selfPlayers = []
matchs = []

class MyConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		# self.matchId = self.scope["url_route"]["kwargs"]["match_id"]    
		print(f"new user connection for match", flush=True)
		await self.accept() 
		self.id = len(players) + 1
		players.append({'playerId': self.id})
		selfPlayers.append({'playerId': self.id, 'socket': self})
		await self.send(text_data=json.dumps({"type": "selfAssign", "selfId": self.id})) 
		for selfplay in selfPlayers:
			await selfplay['socket'].send(text_data=json.dumps({"type": "playerList", "players": players})) #change for channels

	async def disconnect(self, close_code):
		global selfPlayers
		print(f"tournament disconnected id:{self.id}", flush=True)
		for p in selfPlayers: 
			if p['socket'] == self:
				print(p['playerId'], flush=True)
		selfPlayers = [p for p in selfPlayers if p['socket'] != self]
		for selfplay in selfPlayers:
			await selfplay['socket'].send(text_data=json.dumps({"type": "playerList", "players": players})) 
		
	async def receive(self, text_data):
		
		data = json.loads(text_data)
		print(f"new message on serv: {data}", flush=True)
		# if data.get('type') == "invitation":			
		# 	for p in selfPlayers: 
		# 		if p['playerId'] == data['choosenId']:
		# 			await p['socket'].send(text_data=json.dumps({"type": "invitation", "player": self.id}))
		# elif data.get('type') == "cancelInvitation":			
		# 	for p in selfPlayers: 
		# 		if p['playerId'] == data['choosenId']:
		# 			await p['socket'].send(text_data=json.dumps({"type": "cancelInvitation", "player": self.id}))
		# elif data.get('type') == "confirmation":			
		# 	for p in selfPlayers: 
		# 		if p['playerId'] == data['applicantId']:
		# 			await p['socket'].send(text_data=json.dumps({"type": "confirmation", "response": data['response'], "choosen": self.id}))
		# elif data.get('matchId') is not None:
		# 	print(f"{data['matchId']} is not None", flush=True)
		# 	for p in selfPlayers: 
		# 		if p['playerId'] == data['choosenId']:
		# 			await p['socket'].send(text_data=json.dumps({"matchId": data['matchId']}))

		match data:			
			case {"type": "invitation"}:
				for p in selfPlayers:
					if p['playerId'] == data['choosenId']:
						await p['socket'].send(text_data=json.dumps({"type": "invitation", "player": self.id}))

			case {"type": "cancelInvitation"}:
				for p in selfPlayers:
					if p['playerId'] == data['choosenId']:
						await p['socket'].send(text_data=json.dumps({"type": "cancelInvitation", "player": self.id}))

			case {"type": "confirmation", "response": response, **rest}:
				for p in selfPlayers:
					if p['playerId'] == data['applicantId']:
						await p['socket'].send(text_data=json.dumps({"type": "confirmation", "response": response, "choosen": self.id}))

			case _ if data.get("matchId") is not None:
				print(f"{data['matchId']} is not None", flush=True)
				for p in selfPlayers:
					if p['playerId'] == data['choosenId']:
						await p['socket'].send(text_data=json.dumps({"matchId": data['matchId']}))
			case _:
				pass  

		# print(
		# 	f"ici houston, voila l'action {data.get('action')}, \
		# 		et puis voila la direction {data.get('direction')}\n"
		# )
		# for p in players: 
		# 	if p['socket'] == self:
		# 		p['dir'] = data.get('dir')
				# print('is talking', p['id'], flush=True)
	
		# await self.send(
		# 	text_data=json.dumps(
		# 		f"from server ici houston, \
		# 							on a recu ça {text_data}"
		# 	)
	# )  # Envoie une réponse
