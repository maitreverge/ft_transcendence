import threading
import time

import match_app.services.consumer as consumer

import asyncio
import json
from enum import Enum
# class Pong:

# 	id = 0
# 	def __init__(self):
# 		Pong.id += 1
# 		self.id = Pong.id
# 		# self.players = players
# 		threading.Thread(target=self.launch, daemon=True).start()

# 	def launch(self):
# 		while (True):			
# 			print(f"game state {self.id}" , flush=True)
# 			self.sendState()
# 			time.sleep(1)

# 	def sendState(self):
# 		print(consumer.players)
# 		self.myplayers = [p for p in consumer.players if self.id == p["matchId"]]
# 		print(self.myplayers)
# 		for p in self.myplayers:	
# 			print(f"send state {self.id}", flush=True)
# 			p["socket"].send(text_data="youhou")

class State(Enum):
	waiting = "waiting"
	running = "running"
	end = "end"

class Pong:

	id = 0
	def __init__(self, idP1, idP2):
		Pong.id += 1
		self.id = Pong.id
		self.idP1 = idP1
		self.idP2 = idP2
		self.yp1 = 0
		self.yp2 = 0
		self.winner = None

		print("launch init", flush=True)

		# asyncio.run(self.end())
		threading.Thread(target=self.launchTask, daemon=True).start()

	# async def end(self):
	# 	print("end un", flush=True)
	# 	await self.two()
	# 	print("end deux", flush=True)
		
	# async def two(self):
	# 	print("two un", flush=True)
	# 	await self.three()
	# 	print("two deux", flush=True)
		
	# async def three(self):
	# 	print("three un", flush=True)
	# 	await asyncio.sleep(1)
	# 	print("three deux", flush=True)
		

	def launchTask(self):
		print("launch task", flush=True)
		self.myEventLoop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.myEventLoop)
		self.myEventLoop.create_task(self.launch())
		# self.myEventLoop.run_forever()
		# myEventLoop.run_until_complete(asyncio.Future())
		self.myEventLoop.run_until_complete(self.launch())

	async def launch(self):
		self.state = State.waiting
		self.myEventLoop.create_task(self.sendState())
		while self.state in (State.running, State.waiting):		
		
			self.myplayers = [p for p in consumer.players if self.id == p["matchId"]]
			self.player1 = next((p for p in self.myplayers if self.idP1 == p["playerId"]), None)
			self.player2 = next((p for p in self.myplayers if self.idP2 == p["playerId"]), None)
			if None not in (self.player1, self.player2):
				self.state = State.running
				if self.player1.get("dir") is not None :
					if self.player1["dir"] == 'up':
						self.yp1 -= 1
					elif self.player1["dir"] == 'down':
						self.yp1 += 1
					self.player1["dir"] = None
				if  self.player2.get("dir") is not None :
					if self.player2["dir"] == 'up':
						self.yp2 -= 1
					elif self.player2["dir"] == 'down':
						self.yp2 += 1
					self.player2["dir"] = None
			else:
				self.state = State.waiting
			
			if self.yp1 > 80:		
				self.winner = self.idP1
				self.state = State.end
				await self.sendState()
				print("TU DEVRAIS ME VOIR", flush=True)
			elif self.yp2 > 80:
				self.winner = self.idP2
				self.state = State.end
				await self.sendState()
				print("TU DEVRAIS ME VOIR", flush=True)
					
			await asyncio.sleep(0.05)
		print("FIN DU WHIIIIILEEEEEEE", flush=True)
	
	async def sendState(self):		
		while (True):	
			self.myplayers = [p for p in consumer.players if self.id == p["matchId"]]

			for p in self.myplayers:	
				await p["socket"].send(text_data=json.dumps({"state": self.state.name, "yp1": self.yp1, "yp2": self.yp2, "winner": self.winner}))
			await asyncio.sleep(0.05)



# class Pong:
#     id = 0
#     def __init__(self):
#         Pong.id += 1
#         self.id = Pong.id
#         # On lance la coroutine dans l'event loop, qui doit être déjà active
#         asyncio.create_task(self.launch())

#     async def launch(self):
#         while True:
#             print(f"game state {self.id}", flush=True)
#             await self.sendState()
#             await asyncio.sleep(1)

#     async def sendState(self):
#         print(consumer.players)
#         self.myplayers = [p for p in consumer.players if self.id == int(p["matchId"])]
#         print(self.myplayers)
#         # Lancer les envois sans attendre chaque envoi (fire-and-forget)
#         for p in self.myplayers:
#             print(f"send state {self.id}", flush=True)
#             # Ici on peut créer une tâche pour envoyer le message sans attendre sa fin
#             asyncio.create_task(p["socket"].send(text_data="youhou"))
# import types
# class Pong:
# 	id = 0
# 	def __init__(self):
# 		Pong.id += 1
# 		self.id = Pong.id
# 		# On lance la coroutine dans l'event loop, qui doit être déjà active
# 		asyncio.create_task(self.f())

# 	def mon_generateur(self):
# 		yield "première valeur"   # La fonction retourne "première valeur" et se suspend ici
# 		yield "deuxième valeur"   # Au prochain appel, elle reprend ici et retourne "deuxième valeur"
# 		yield "troisième valeur"  # Et ainsi de suite

   	
# 	async def f(self):
# 		# print("début", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre1", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre2", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre3", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre4", flush=True)
# 		# On lance la tâche foo en parallèle
# 		asyncio.create_task(self.foo())
# 		# await asyncio.sleep(0)
		
# 		await self.launch()  # On attend la fin de launch()
# 		print("fin", flush=True)
		
# 	@types.coroutine
# 	def launch(self):
# 		yield
# 		print("launch", flush=True)	
# 		# await self.truc()    # On attend que truc() se termine
# 		print("launch2", flush=True)
# 		print("launch3", flush=True)

# 	async def truc(self):
# 		print("truc", flush=True)

# 	async def foo(self):
# 		print("foo", flush=True)
