
class Tournament():
	
	id = 0
	def __init__(self, applicantId):

		Tournament.id += 1
		self.id = Tournament.id
		self.players = []

	def append(self, player):
		self.players.append(player)