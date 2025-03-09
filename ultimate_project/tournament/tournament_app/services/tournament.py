import json

class Tournament():
	
	id = 0
	def __init__(self, applicantId):

		Tournament.id += 1
		self.id = Tournament.id
		self.players = []

	async def append(self, player):
		self.players.append(player)
		if len(self.players) >= 2:
			for player in self.players:				
				await player.send(text_data=json.dumps({
					"type": "getPattern",
					"tournamentId": self.id					
				}))

	def remove(self, player):
		self.players[:] = [p for p in self.players if p != player]
		