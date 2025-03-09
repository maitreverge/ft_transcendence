
class Tournament():
	
	id = 0
	def __init__(self, applicantId):

		Tournament.id += 1
		self.id = Tournament.id
		self.players = []

	def append(self, player):
		self.players.append(player)

	def remove(self, player):
		self.players[:] = [p for p in self.players if p != player]
		