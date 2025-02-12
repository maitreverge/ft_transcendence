import threading
import time

class Pong:

	id = 0
	def __init__(self):
		Pong.id += 1
		self.id = Pong.id
		# self.players = players
		threading.Thread(target=self.launch, daemon=True).start()

	def launch(self):
		while (True):			
			print(f"game state {self.id}" , flush=True)
			self.sendState()
			time.sleep(1)

	def sendState(self):
		print(f"send state {self.id}", flush=True)
